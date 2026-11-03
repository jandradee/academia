from rest_framework import viewsets
from .models import AuditLog
from .serializers import AuditLogSerializer
from apps.users.permissions import IsAdminPlatform
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=AuditLog.objects.all(); serializer_class=AuditLogSerializer; permission_classes=[IsAdminPlatform]; filterset_fields=["action","entity_type","actor"]
