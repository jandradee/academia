import uuid
from django.db import models
from django.conf import settings
class AuditLog(models.Model):
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True); action=models.CharField(max_length=100,db_index=True); entity_type=models.CharField(max_length=100,blank=True); entity_id=models.CharField(max_length=100,blank=True); occurred_at=models.DateTimeField(auto_now_add=True,db_index=True); result=models.CharField(max_length=30,default="ok"); correlation_id=models.UUIDField(default=uuid.uuid4); details_redacted=models.JSONField(default=dict,blank=True)
    class Meta: ordering=["-occurred_at"]
class AppSetting(models.Model):
    key=models.CharField(max_length=100,unique=True); value=models.JSONField(default=dict); updated_at=models.DateTimeField(auto_now=True)
    # NUNCA guardar secretos aquí (RNF-001.1)
