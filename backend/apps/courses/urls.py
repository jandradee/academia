from rest_framework.routers import DefaultRouter
from .views import *
router=DefaultRouter(); router.register("categories",CategoryViewSet); router.register("courses",CourseViewSet); router.register("modules",ModuleViewSet); router.register("videos",VideoViewSet); router.register("resources",ResourceViewSet); router.register("assignments",AssignmentViewSet); router.register("enrollments",EnrollmentViewSet)
urlpatterns=router.urls
