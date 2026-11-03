import uuid
from django.db import models
from django.conf import settings
class Certificate(models.Model):
    certificate_uuid=models.UUIDField(default=uuid.uuid4,unique=True,editable=False); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="certificates"); course=models.ForeignKey("courses.Course",on_delete=models.CASCADE,related_name="certificates"); course_version=models.PositiveIntegerField(default=1); issued_at=models.DateTimeField(auto_now_add=True); completion_date=models.DateField(null=True,blank=True); recognized_duration_minutes=models.PositiveIntegerField(default=0); file_key=models.CharField(max_length=500,blank=True); status=models.CharField(max_length=30,default="emitido"); template_version=models.CharField(max_length=20,default="1.0")
    class Meta: unique_together=("user","course","course_version")
class Notification(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="notifications"); notification_type=models.CharField(max_length=50); idempotency_key=models.CharField(max_length=200,unique=True); status=models.CharField(max_length=30,default="pendiente"); attempt_count=models.PositiveIntegerField(default=0); next_attempt_at=models.DateTimeField(null=True,blank=True); sent_at=models.DateTimeField(null=True,blank=True); last_error=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True)
