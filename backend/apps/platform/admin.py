from django.contrib import admin
from .models import SiteSettings, CourseRating
admin.site.register([SiteSettings, CourseRating])
