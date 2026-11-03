from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import branding, branding_admin, branding_logo, reports_overview, reports_export_xlsx, reports_dashboard, reports_dashboard_xlsx, CourseRatingViewSet, my_rating
router = DefaultRouter(); router.register("ratings", CourseRatingViewSet)
urlpatterns = [
    path("branding/", branding),
    path("branding/admin/", branding_admin),
    path("branding/logo/", branding_logo),
    path("reports/overview/", reports_overview),
    path("reports/export.xlsx", reports_export_xlsx),
    path("reports/dashboard/", reports_dashboard),
    path("reports/dashboard.xlsx", reports_dashboard_xlsx),
    path("courses/<int:course_id>/my-rating/", my_rating),
] + router.urls
