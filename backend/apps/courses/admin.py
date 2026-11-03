from django.contrib import admin
from .models import *
admin.site.register([Category,Course,Module,Video,Resource,Assignment,Enrollment,FileAsset])
