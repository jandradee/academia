from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, RoleViewSet, SyncRunViewSet
router=DefaultRouter(); router.register("users",UserViewSet); router.register("roles",RoleViewSet); router.register("sync-runs",SyncRunViewSet)
from .views import me, my_avatar
urlpatterns=[path("token/",TokenObtainPairView.as_view(),name="token_obtain_pair"),path("token/refresh/",TokenRefreshView.as_view(),name="token_refresh"),path("me/",me),path("me/avatar/",my_avatar),path("",include(router.urls))]
