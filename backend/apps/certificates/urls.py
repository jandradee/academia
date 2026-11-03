from rest_framework.routers import DefaultRouter
from .views import CertificateViewSet, NotificationViewSet
router=DefaultRouter(); router.register("certificates",CertificateViewSet); router.register("notifications",NotificationViewSet)
urlpatterns=router.urls
