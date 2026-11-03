from django.contrib import admin
from .models import *
admin.site.register([Quiz,Question,Option,Attempt,Answer])
