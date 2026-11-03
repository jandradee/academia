from django.contrib import admin
from .models import User, Role, UserRole, SyncRun
admin.site.register([User,Role,UserRole,SyncRun])
