from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Certificate, Notification
from .serializers import CertificateSerializer, NotificationSerializer
class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Certificate.objects.all(); serializer_class=CertificateSerializer; permission_classes=[IsAuthenticated]; filterset_fields=["user","course","status"]
    def get_queryset(self):
        qs=super().get_queryset(); return qs if self.request.user.is_superuser else qs.filter(user=self.request.user)
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=Notification.objects.all(); serializer_class=NotificationSerializer; permission_classes=[IsAuthenticated]
    def get_queryset(self):
        qs=super().get_queryset()
        return qs if self.request.user.is_superuser else qs.filter(user=self.request.user)
