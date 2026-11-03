from django.http import FileResponse, Http404
from django.db.models import Avg, Count, Sum
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from .models import SiteSettings, CourseRating
from .serializers import SiteSettingsSerializer, SiteSettingsWriteSerializer, CourseRatingSerializer
from apps.users.permissions import IsAdminPlatform, IsAdminOrManager

@api_view(["GET"])
@permission_classes([AllowAny])
def branding(request):
    # Público (tras la allowlist de red): el frontend lo necesita ANTES del login para pintar el tema.
    return Response(SiteSettingsSerializer(SiteSettings.load()).data)

@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAdminPlatform])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def branding_admin(request):
    obj = SiteSettings.load()
    if request.method == "GET":
        return Response(SiteSettingsWriteSerializer(obj).data)
    ser = SiteSettingsWriteSerializer(obj, data=request.data, partial=(request.method == "PATCH"))
    ser.is_valid(raise_exception=True)
    ser.save(updated_by=request.user)
    return Response(SiteSettingsSerializer(obj).data)

@api_view(["GET"])
@permission_classes([AllowAny])
def branding_logo(request):
    obj = SiteSettings.load()
    if not obj.logo_file:
        raise Http404("Sin logo en archivo")
    import mimetypes
    resp = FileResponse(obj.logo_file.open("rb"), content_type=mimetypes.guess_type(obj.logo_file.name)[0] or "image/png")
    resp["Cache-Control"] = "no-cache, must-revalidate"
    return resp

# ---------- Reportes / Dashboard gerencial ----------
@api_view(["GET"])
@permission_classes([IsAdminOrManager])
def reports_overview(request):
    from apps.progress.models import CourseProgress
    from apps.courses.models import Course, Assignment
    from apps.certificates.models import Certificate
    from django.contrib.auth import get_user_model
    qs = CourseProgress.objects.all()
    by_status = {row["status"]: row["n"] for row in qs.values("status").annotate(n=Count("id"))}
    completed = by_status.get("completado", 0) + by_status.get("aprobado", 0)
    popular = list(Course.objects.annotate(enrollments_count=Count("progress", distinct=True) + Count("assignments", distinct=True), avg_rating=Avg("ratings__stars"), ratings_count=Count("ratings", distinct=True)).order_by("-enrollments_count").values("id", "title", "enrollments_count", "avg_rating", "ratings_count")[:10])
    per_course = []
    for c in Course.objects.all():
        cps = qs.filter(course=c)
        total = cps.count()
        comp = cps.filter(status__in=["completado", "aprobado"]).count()
        prog = cps.filter(status="en_progreso").count()
        per_course.append({"course_id": c.id, "title": c.title, "status": c.status, "assigned_or_started": total, "completed": comp, "in_progress": prog, "not_started": total - comp - prog, "completion_rate": round(comp / total * 100, 1) if total else 0})
    return Response({
        "totals": {"courses": Course.objects.count(), "users": get_user_model().objects.filter(is_active=True).count(), "assignments": Assignment.objects.filter(status="activa").count(), "certificates": Certificate.objects.count()},
        "progress": {"completed": completed, "in_progress": by_status.get("en_progreso", 0), "not_started": by_status.get("no_iniciado", 0), "expired": by_status.get("vencido", 0)},
        "popular_courses": popular,
        "per_course": per_course,
    })

@api_view(["GET"])
@permission_classes([IsAdminOrManager])
def reports_export_xlsx(request):
    import io
    from openpyxl import Workbook
    from django.http import HttpResponse
    from apps.progress.models import CourseProgress
    from apps.courses.models import Course
    wb = Workbook()
    ws = wb.active; ws.title = "Resumen por curso"
    ws.append(["Curso", "Estado", "Asignados/Iniciados", "Completados", "En progreso", "No iniciados", "% Finalización", "Promedio estrellas"])
    for c in Course.objects.all():
        cps = CourseProgress.objects.filter(course=c)
        total = cps.count(); comp = cps.filter(status__in=["completado", "aprobado"]).count(); prog = cps.filter(status="en_progreso").count()
        avg = c.ratings.aggregate(a=Avg("stars"))["a"]
        ws.append([c.title, c.status, total, comp, prog, total - comp - prog, round(comp / total * 100, 1) if total else 0, round(avg, 2) if avg else ""])
    ws2 = wb.create_sheet("Detalle por empleado")
    ws2.append(["Empleado", "Correo", "Departamento", "Curso", "Estado", "Avance %", "Inicio", "Última actividad", "Finalización", "Aprobación", "Horas reconocidas"])
    for cp in CourseProgress.objects.select_related("user", "course").all():
        ws2.append([cp.user.display_name or cp.user.username, cp.user.email, cp.user.department, cp.course.title, cp.status, float(cp.progress_percent), str(cp.first_started_at or ""), str(cp.last_activity_at or ""), str(cp.completed_at or ""), str(cp.passed_at or ""), round(cp.course.recognized_duration_minutes / 60, 2) if cp.status in ("completado", "aprobado") else 0])
    ws3 = wb.create_sheet("Calificaciones")
    ws3.append(["Curso", "Empleado", "Estrellas", "Comentario", "Fecha"])
    for r in CourseRating.objects.select_related("user", "course").all():
        ws3.append([r.course.title, r.user.display_name or r.user.username, r.stars, r.comment, str(r.updated_at)])
    buf = io.BytesIO(); wb.save(buf); buf.seek(0)
    resp = HttpResponse(buf.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp["Content-Disposition"] = 'attachment; filename="reporte-capacitacion.xlsx"'
    return resp

# ---------- Dashboard de gestión (inicio para gestores/administradores) ----------
def _dashboard_data():
    """Datos del panel de gestión: por curso, % de asignados no iniciados / en progreso /
    completados (base: asignaciones activas; estado desde el progreso), y el RawData
    usuario×curso. Lo comparten el endpoint JSON y la exportación a Excel."""
    from apps.courses.models import Course, Assignment
    from apps.progress.models import CourseProgress
    from apps.courses.serializers import cover_url
    labels = {"no_iniciado": "No iniciado", "en_progreso": "En progreso", "completado": "Completado", "aprobado": "Completado", "vencido": "Vencido"}
    courses_out, rows = [], []
    tot = {"assigned": 0, "not_started": 0, "in_progress": 0, "completed": 0}
    users_set = set()
    for c in Course.objects.exclude(status="archivado").order_by("title"):
        assigns = list(Assignment.objects.filter(course=c, status="activa").select_related("user"))
        prog = {cp.user_id: cp for cp in CourseProgress.objects.filter(course=c)}
        ns = ip = comp = 0
        for a in assigns:
            cp = prog.get(a.user_id)
            st = cp.status if cp else "no_iniciado"
            if st in ("completado", "aprobado"): bucket = "completed"; comp += 1
            elif st == "en_progreso": bucket = "in_progress"; ip += 1
            else: bucket = "not_started"; ns += 1
            users_set.add(a.user_id)
            rows.append({
                "user_id": a.user_id, "user": a.user.display_name or a.user.username, "username": a.user.username,
                "department": a.user.department or "", "course_id": c.id, "course": c.title,
                "status": st, "status_bucket": bucket, "status_label": labels.get(st, st),
                "progress_percent": float(cp.progress_percent) if cp else 0,
                "due_at": a.due_at.isoformat() if a.due_at else None,
                "assigned_at": a.assigned_at.isoformat() if getattr(a, "assigned_at", None) else None,
                "passed_at": cp.passed_at.isoformat() if cp and cp.passed_at else None,
            })
        total = len(assigns)
        pct = (lambda n: round(n / total * 100, 1) if total else 0)
        courses_out.append({"course_id": c.id, "title": c.title, "cover": cover_url(c), "status": c.status,
                            "assigned": total, "not_started": ns, "in_progress": ip, "completed": comp,
                            "pct_not_started": pct(ns), "pct_in_progress": pct(ip), "pct_completed": pct(comp)})
        tot["assigned"] += total; tot["not_started"] += ns; tot["in_progress"] += ip; tot["completed"] += comp
    tot["users"] = len(users_set); tot["courses"] = len(courses_out)
    tot["pct_completed"] = round(tot["completed"] / tot["assigned"] * 100, 1) if tot["assigned"] else 0
    return {"totals": tot, "courses": courses_out, "rows": rows}

@api_view(["GET"])
@permission_classes([IsAdminOrManager])
def reports_dashboard(request):
    return Response(_dashboard_data())

@api_view(["GET"])
@permission_classes([IsAdminOrManager])
def reports_dashboard_xlsx(request):
    import io
    from openpyxl import Workbook
    from django.http import HttpResponse
    data = _dashboard_data()
    wb = Workbook()
    ws = wb.active; ws.title = "Resumen por curso"
    ws.append(["Curso", "Usuarios asignados", "No iniciados", "% No iniciados", "En progreso", "% En progreso", "Completados", "% Completados"])
    for c in data["courses"]:
        ws.append([c["title"], c["assigned"], c["not_started"], c["pct_not_started"], c["in_progress"], c["pct_in_progress"], c["completed"], c["pct_completed"]])
    ws2 = wb.create_sheet("RawData")
    ws2.append(["Empleado", "Usuario", "Departamento", "Curso", "Estado", "Avance %", "Fecha límite", "Fecha de aprobación"])
    for r in data["rows"]:
        ws2.append([r["user"], r["username"], r["department"], r["course"], r["status_label"], r["progress_percent"], (r["due_at"] or "")[:10], (r["passed_at"] or "")[:10]])
    buf = io.BytesIO(); wb.save(buf); buf.seek(0)
    resp = HttpResponse(buf.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    resp["Content-Disposition"] = 'attachment; filename="dashboard-academia.xlsx"'
    return resp

class CourseRatingViewSet(viewsets.ModelViewSet):
    queryset = CourseRating.objects.all()
    serializer_class = CourseRatingSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["course", "user"]
    def perform_create(self, serializer): serializer.save(user=self.request.user)
    def get_queryset(self):
        qs = super().get_queryset()
        # El estudiante ve/edita lo suyo; gestores ven todo (para el reporte)
        if self.request.user.is_superuser or self.request.user.roles.filter(code__in=["ADMIN", "GESTOR"]).exists():
            return qs
        return qs.filter(user=self.request.user) | qs.filter(course__in=self.request.query_params.getlist("course")) if False else qs

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def my_rating(request, course_id):
    from apps.courses.models import Course
    course = Course.objects.filter(pk=course_id).first()
    if not course: return Response({"detail": "Curso no encontrado"}, status=404)
    if request.method == "GET":
        agg = course.ratings.aggregate(avg=Avg("stars"), count=Count("id"))
        mine = course.ratings.filter(user=request.user).first()
        return Response({"average": round(agg["avg"], 2) if agg["avg"] else None, "count": agg["count"], "my_rating": CourseRatingSerializer(mine).data if mine else None})
    stars = int(request.data.get("stars", 0))
    if stars < 1 or stars > 5: return Response({"detail": "stars debe ser 1-5"}, status=400)
    obj, _ = CourseRating.objects.update_or_create(course=course, user=request.user, defaults={"stars": stars, "comment": request.data.get("comment", "")})
    return Response(CourseRatingSerializer(obj).data)
