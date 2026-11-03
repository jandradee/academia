from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def health(_): return JsonResponse({"status":"ok","service":"lms-api","framework":"Django REST Framework"})

urlpatterns = [
    path("health/", health),
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/", include("apps.users.urls_auth")),
    path("api/", include("apps.courses.urls")),
    path("api/", include("apps.quizzes.urls")),
    path("api/", include("apps.progress.urls")),
    path("api/", include("apps.certificates.urls")),
    path("api/", include("apps.audit.urls")),
    path("api/", include("apps.platform.urls")),
]
