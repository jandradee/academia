from django.contrib.auth.models import AbstractUser
from django.db import models
class Role(models.Model):
    code=models.CharField(max_length=50,unique=True)
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    def __str__(self): return self.code
class User(AbstractUser):
    entra_object_id=models.CharField(max_length=64,unique=True,null=True,blank=True,db_index=True)
    display_name=models.CharField(max_length=255,blank=True)
    department=models.CharField(max_length=150,blank=True,db_index=True)
    job_title=models.CharField(max_length=150,blank=True)
    office_location=models.CharField(max_length=150,blank=True)
    last_synced_at=models.DateTimeField(null=True,blank=True)
    avatar=models.FileField(upload_to="avatars/",null=True,blank=True)
    language=models.CharField(max_length=5,default="es")
    email_notifications=models.BooleanField(default=True)
    roles=models.ManyToManyField(Role,through="UserRole",through_fields=("user","role"),related_name="users",blank=True)
    class Meta: ordering=["display_name","username"]
class UserRole(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    role=models.ForeignKey(Role,on_delete=models.CASCADE)
    assigned_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="role_assignments_made")
    assigned_at=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=("user","role")
class SyncRun(models.Model):
    started_at=models.DateTimeField(auto_now_add=True)
    finished_at=models.DateTimeField(null=True,blank=True)
    status=models.CharField(max_length=30,default="running")
    users_read=models.IntegerField(default=0); users_created=models.IntegerField(default=0)
    users_updated=models.IntegerField(default=0); users_deactivated=models.IntegerField(default=0)
    errors_summary=models.TextField(blank=True)
