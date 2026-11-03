from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum
from .models import CourseProgress, ModuleProgress, VideoProgress, ResourceProgress
from .serializers import *
def _own_or_all(qs, user):
    # Los registros de aprendizaje son personales: cada usuario ve solo los suyos.
    # (Los gestores consultan agregados en los reportes, no los registros individuales.)
    if user.is_superuser: return qs
    return qs.filter(user=user)

class CourseProgressViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return _own_or_all(super().get_queryset(), self.request.user)
    queryset=CourseProgress.objects.all(); serializer_class=CourseProgressSerializer; permission_classes=[IsAuthenticated]; filterset_fields=["course","user","status"]
class ResourceProgressViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return _own_or_all(super().get_queryset(), self.request.user)
    queryset=ResourceProgress.objects.all(); serializer_class=ResourceProgressSerializer; permission_classes=[IsAuthenticated]; filterset_fields=["resource","user"]
class ModuleProgressViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return _own_or_all(super().get_queryset(), self.request.user)
    queryset=ModuleProgress.objects.all(); serializer_class=ModuleProgressSerializer; permission_classes=[IsAuthenticated]
class VideoProgressViewSet(viewsets.ModelViewSet):
    def get_queryset(self): return _own_or_all(super().get_queryset(), self.request.user)
    queryset=VideoProgress.objects.all(); serializer_class=VideoProgressSerializer; permission_classes=[IsAuthenticated]
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_dashboard(request):
    # RF-014: inicio del colaborador + horas del año calendario (duración reconocida, una sola vez al aprobar)
    from django.utils import timezone
    year=timezone.now().year
    qs=CourseProgress.objects.filter(user=request.user)
    hours=qs.filter(status="aprobado",passed_at__year=year).aggregate(t=Sum("course__recognized_duration_minutes"))["t"] or 0
    from apps.courses.models import Assignment
    from apps.certificates.models import Certificate
    from apps.certificates.serializers import CertificateSerializer
    months=[0]*12
    for cp in qs.filter(status="aprobado",passed_at__year=year):
        months[cp.passed_at.month-1]+=cp.course.recognized_duration_minutes
    mandatory_pending = Assignment.objects.filter(user=request.user, status="activa", is_mandatory=True).exclude(course__in=qs.filter(status__in=["en_progreso","completado","aprobado"]).values_list("course", flat=True)).count()
    certs = Certificate.objects.filter(user=request.user).order_by("-issued_at")
    return Response({"pending":qs.filter(status__in=["no_iniciado","en_progreso"]).count(),"in_progress":qs.filter(status="en_progreso").count(),"completed":qs.filter(status__in=["completado","aprobado"]).count(),"mandatory_pending":mandatory_pending,"certificates_count":certs.count(),"certificates":CertificateSerializer(certs, many=True).data,"training_hours_current_year":round(hours/60,2),"training_minutes_current_year":hours,"hours_by_month":[round(m/60,2) for m in months],"minutes_by_month":months})
