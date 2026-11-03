from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
import os, uuid
from django.conf import settings
from django.http import Http404, FileResponse
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Category, Course, Module, Video, Resource, Assignment, Enrollment, FileAsset

def _save_upload(request, folder, allowed_exts):
    f = request.FILES.get("file")
    if not f: return None, Response({"detail": "Falta el archivo (campo file)"}, status=400)
    ext = os.path.splitext(f.name)[1].lower()
    if ext not in allowed_exts: return None, Response({"detail": f"Extensión no permitida: {ext}"}, status=400)
    if f.size > 2 * 1024 * 1024 * 1024: return None, Response({"detail": "Archivo demasiado grande (máx 2 GB)"}, status=400)
    key = f"{folder}/{uuid.uuid4().hex}{ext}"
    dest = os.path.join(str(settings.MEDIA_ROOT), key)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb+") as out:
        for chunk in f.chunks(): out.write(chunk)
    asset = FileAsset.objects.create(storage_key=key, original_name=f.name, mime_type=f.content_type or "", size_bytes=f.size, uploaded_by=request.user)
    return (key, asset), None
from .serializers import *
from apps.users.permissions import IsAdminOrManager
class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all(); serializer_class=CategorySerializer; permission_classes=[IsAuthenticated]
class CourseViewSet(viewsets.ModelViewSet):
    queryset=Course.objects.all().prefetch_related("modules__videos","modules__resources"); permission_classes=[IsAuthenticated]; filterset_fields=["status","course_type","category"]; search_fields=["title","code","short_description"]
    def get_permissions(self):
        if self.action == "cover_image": return []
        if self.action in ("list","retrieve"): return [IsAuthenticated()]
        return [IsAdminOrManager()]
    @action(detail=True, methods=["post"], parser_classes=[MultiPartParser, FormParser])
    def cover(self, request, pk=None):
        course = self.get_object()
        f = request.FILES.get("file")
        if not f: return Response({"detail": "Falta el archivo (campo file)."}, status=400)
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in [".png", ".jpg", ".jpeg", ".webp", ".gif"]: return Response({"detail": "Formato no admitido (usa PNG/JPG/WebP)."}, status=400)
        if f.size > 10 * 1024 * 1024: return Response({"detail": "La imagen supera 10 MB."}, status=400)
        key = f"covers/{uuid.uuid4().hex}{ext}"
        dest = os.path.join(str(settings.MEDIA_ROOT), key); os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as out:
            for chunk in f.chunks(): out.write(chunk)
        course.cover_key = key; course.save(update_fields=["cover_key"])
        return Response(CourseSerializer(course).data)
    @action(detail=True, methods=["get"], permission_classes=[], url_path="cover-image")
    def cover_image(self, request, pk=None):
        from apps.core.files import media_path
        course = self.get_object()
        if not course.cover_key: raise Http404("Sin imagen")
        path = media_path(course.cover_key)
        if not os.path.exists(path): raise Http404("Imagen no encontrada")
        import mimetypes
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        resp = FileResponse(open(path, "rb"), content_type=ctype)
        resp["Cache-Control"] = "no-cache, must-revalidate"
        return resp
    def get_serializer_class(self): return CourseListSerializer if self.action=="list" else CourseSerializer
    def get_queryset(self):
        qs=super().get_queryset()
        u=self.request.user
        if getattr(u, "is_authenticated", False) and (u.is_superuser or u.roles.filter(code__in=["ADMIN","GESTOR"]).exists()):
            return qs
        return qs.filter(status="publicado")
class ModuleViewSet(viewsets.ModelViewSet):
    queryset=Module.objects.all(); serializer_class=ModuleSerializer; permission_classes=[IsAdminOrManager]; filterset_fields=["course"]
class VideoViewSet(viewsets.ModelViewSet):
    queryset=Video.objects.all(); serializer_class=VideoSerializer; permission_classes=[IsAuthenticated]; filterset_fields=["module"]
    def get_permissions(self):
        if self.action == "stream": return []  # la vista se autentica sola (header o ?token=, necesario para <video>)
        if self.action in ("retrieve", "list", "report"): return [IsAuthenticated()]
        return [IsAdminOrManager()]
    @action(detail=False, methods=["post"], parser_classes=[MultiPartParser, FormParser], permission_classes=[IsAdminOrManager])
    def upload(self, request):
        saved, err = _save_upload(request, "videos", [".mp4", ".webm", ".mov", ".mkv"])
        if err: return err
        key, asset = saved
        video = Video.objects.create(module_id=request.data.get("module"), title=request.data.get("title") or asset.original_name, description=request.data.get("description", ""), storage_key=key, duration_seconds=int(request.data.get("duration_seconds") or 0), sort_order=int(request.data.get("sort_order") or 0), is_required=True)
        return Response(VideoSerializer(video).data, status=201)
    @action(detail=True, methods=["get"], permission_classes=[])
    def stream(self, request, pk=None):
        from apps.core.files import authenticate_request, range_file_response, media_path
        user = authenticate_request(request)
        if not user: return Response({"detail": "Autenticación requerida"}, status=401)
        video = self.get_object()
        if not video.storage_key: raise Http404("Video sin archivo")
        return range_file_response(request, media_path(video.storage_key), content_type="video/mp4")
    @action(detail=True, methods=["post"])
    def report(self, request, pk=None):
        # Reporte de avance real del video desde el reproductor del estudiante.
        from apps.progress.models import VideoProgress
        from apps.progress.services import recompute_course_progress
        from django.utils import timezone
        video = self.get_object()
        try: pos = int(float(request.data.get("position_seconds") or 0))
        except (TypeError, ValueError): pos = 0
        dur = int(request.data.get("duration_seconds") or 0)
        if dur and not video.duration_seconds:
            video.duration_seconds = dur; video.save(update_fields=["duration_seconds"])
        vp, _ = VideoProgress.objects.get_or_create(video=video, user=request.user)
        vp.last_position_seconds = pos
        if pos > vp.max_position_seconds: vp.max_position_seconds = pos
        if video.duration_seconds and vp.max_position_seconds >= 0.95 * video.duration_seconds and not vp.completed_at:
            vp.completed_at = timezone.now()
        vp.save()
        cp = recompute_course_progress(request.user, video.module.course)
        return Response({"video_percent": round(vp.percent, 1), "course_progress_percent": float(cp.progress_percent), "course_status": cp.status})

class ResourceViewSet(viewsets.ModelViewSet):
    queryset=Resource.objects.all(); serializer_class=ResourceSerializer; permission_classes=[IsAuthenticated]; filterset_fields=["module","course"]
    def get_permissions(self):
        if self.action == "download": return []  # la vista se autentica sola (header o ?token=)
        return [IsAuthenticated()]
    @action(detail=False, methods=["post"], parser_classes=[MultiPartParser, FormParser], permission_classes=[IsAdminOrManager])
    def upload(self, request):
        saved, err = _save_upload(request, "resources", [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".zip"])
        if err: return err
        key, asset = saved
        res = Resource.objects.create(module_id=request.data.get("module") or None, course_id=request.data.get("course") or None, title=request.data.get("title") or asset.original_name, description=request.data.get("description", ""), storage_key=key, mime_type=asset.mime_type, size_bytes=asset.size_bytes)
        return Response(ResourceSerializer(res).data, status=201)
    @action(detail=True, methods=["get"], permission_classes=[])
    def download(self, request, pk=None):
        from apps.core.files import authenticate_request, range_file_response, media_path
        user = authenticate_request(request)
        if not user: return Response({"detail": "Autenticación requerida"}, status=401)
        res = self.get_object()
        if not res.storage_key: raise Http404("Recurso sin archivo")
        try:
            from apps.progress.models import ResourceProgress
            from apps.progress.services import recompute_course_progress
            _, created = ResourceProgress.objects.get_or_create(resource=res, user=user)
            if created:
                course = res.course or (res.module.course if res.module else None)
                if course: recompute_course_progress(user, course)
        except Exception:
            pass
        return range_file_response(request, media_path(res.storage_key), content_type=res.mime_type or "application/octet-stream", download_name=res.title)
class AssignmentViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=["post"], permission_classes=[IsAdminOrManager])
    def bulk(self, request):
        # Asignación masiva: un curso a muchos empleados, sin duplicar activas; crea también el registro de progreso.
        from apps.progress.models import CourseProgress
        course_id = request.data.get("course"); user_ids = request.data.get("user_ids") or []
        if not course_id or not user_ids: return Response({"detail": "Se requiere course y user_ids[]"}, status=400)
        created, skipped = [], []
        for uid in user_ids:
            obj, was_created = Assignment.objects.get_or_create(course_id=course_id, user_id=uid, course_version=1, status="activa", defaults={"assigned_by": request.user, "due_at": request.data.get("due_at") or None, "is_mandatory": bool(request.data.get("is_mandatory", True))})
            CourseProgress.objects.get_or_create(course_id=course_id, user_id=uid, course_version=1)
            (created if was_created else skipped).append(uid)
            if was_created:
                try:
                    from django.contrib.auth import get_user_model
                    from apps.core.mailer import send_assignment_email
                    send_assignment_email(get_user_model().objects.get(pk=uid), obj.course, obj.due_at)
                except Exception:
                    pass
        return Response({"created_user_ids": created, "already_assigned_user_ids": skipped, "total": len(user_ids)})
    queryset=Assignment.objects.all(); serializer_class=AssignmentSerializer; permission_classes=[IsAuthenticated]; filterset_fields=["course","user","status"]
    def perform_create(self, serializer):
        obj = serializer.save(assigned_by=self.request.user)
        try:
            from apps.core.mailer import send_assignment_email
            send_assignment_email(obj.user, obj.course, obj.due_at)
        except Exception:
            pass
    def get_queryset(self):
        qs=super().get_queryset()
        return qs if self.request.user.is_superuser else qs.filter(user=self.request.user)
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset=Enrollment.objects.all(); serializer_class=EnrollmentSerializer; permission_classes=[IsAuthenticated]; filterset_fields=["course","user","status"]
    def get_queryset(self):
        qs=super().get_queryset()
        return qs if self.request.user.is_superuser else qs.filter(user=self.request.user)
