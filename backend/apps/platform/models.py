from django.db import models
from django.conf import settings

class SiteSettings(models.Model):
    # Singleton (pk=1): personalización de la plataforma (consola de administración)
    company_name = models.CharField(max_length=150, default="")
    platform_name = models.CharField(max_length=150, default="Academia")
    tagline = models.CharField(max_length=250, blank=True, default="Aprende, crece y comparte")
    primary_color = models.CharField(max_length=7, default="#4F46E5")
    accent_color = models.CharField(max_length=7, default="#F59E0B")
    beige_color = models.CharField(max_length=7, default="#CBD5E1")
    danger_color = models.CharField(max_length=7, default="#DC2626")
    logo_url = models.URLField(blank=True, help_text="URL externa del logo (alternativa a subir archivo)")
    logo_file = models.FileField(upload_to="branding/", blank=True, null=True)
    support_email = models.EmailField(blank=True)
    footer_text = models.CharField(max_length=250, blank=True, default="Plataforma corporativa de capacitación")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
    @property
    def effective_logo_url(self):
        if self.logo_file:
            return f"/api/branding/logo/?v={int(self.updated_at.timestamp()) if self.updated_at else 0}"
        return self.logo_url or ""

class CourseRating(models.Model):
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_ratings")
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ("course", "user")
        ordering = ["-updated_at"]
