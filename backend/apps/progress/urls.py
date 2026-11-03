from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *
router=DefaultRouter(); router.register("course-progress",CourseProgressViewSet); router.register("module-progress",ModuleProgressViewSet); router.register("video-progress",VideoProgressViewSet); router.register("resource-progress",ResourceProgressViewSet)
urlpatterns=router.urls+[path("dashboard/me/",my_dashboard)]
