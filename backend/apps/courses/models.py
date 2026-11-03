from django.db import models
from django.conf import settings
class Category(models.Model):
    name=models.CharField(max_length=120); description=models.TextField(blank=True); sort_order=models.IntegerField(default=0); is_active=models.BooleanField(default=True)
    def __str__(self): return self.name
class FileAsset(models.Model):
    storage_key=models.CharField(max_length=500); original_name=models.CharField(max_length=255); mime_type=models.CharField(max_length=120,blank=True); size_bytes=models.BigIntegerField(default=0); sha256=models.CharField(max_length=64,blank=True); uploaded_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True); status=models.CharField(max_length=30,default="active")
class Course(models.Model):
    class Status(models.TextChoices): DRAFT="borrador","Borrador"; PUBLISHED="publicado","Publicado"; ARCHIVED="archivado","Archivado"; RETIRED="retirado","Retirado"
    class Type(models.TextChoices): MANDATORY="obligatorio","Obligatorio"; OPTIONAL="opcional","Opcional"
    code=models.CharField(max_length=50,unique=True,blank=True,null=True); title=models.CharField(max_length=255); short_description=models.CharField(max_length=500,blank=True); description=models.TextField(blank=True)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name="courses"); course_type=models.CharField(max_length=20,choices=Type.choices,default=Type.OPTIONAL); status=models.CharField(max_length=20,choices=Status.choices,default=Status.DRAFT)
    available_from=models.DateTimeField(null=True,blank=True); available_until=models.DateTimeField(null=True,blank=True)
    estimated_duration_minutes=models.PositiveIntegerField(default=0); recognized_duration_minutes=models.PositiveIntegerField(default=0); cover_key=models.CharField(max_length=500,blank=True); pass_score=models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    version=models.PositiveIntegerField(default=1); created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="courses_created"); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["title"]
    def __str__(self): return self.title
class Module(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="modules"); title=models.CharField(max_length=255); description=models.TextField(blank=True); sort_order=models.IntegerField(default=0); estimated_duration_minutes=models.PositiveIntegerField(default=0); sequential=models.BooleanField(default=False)
    class Meta: ordering=["sort_order"]
class Video(models.Model):
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="videos"); title=models.CharField(max_length=255); description=models.TextField(blank=True); storage_key=models.CharField(max_length=500,blank=True); duration_seconds=models.PositiveIntegerField(default=0); sort_order=models.IntegerField(default=0); is_required=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["sort_order"]
class Resource(models.Model):
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="resources",null=True,blank=True); course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="resources",null=True,blank=True); title=models.CharField(max_length=255); description=models.TextField(blank=True); storage_key=models.CharField(max_length=500,blank=True); mime_type=models.CharField(max_length=120,blank=True); size_bytes=models.BigIntegerField(default=0); version=models.PositiveIntegerField(default=1); is_active=models.BooleanField(default=True)
class Assignment(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="assignments"); course_version=models.PositiveIntegerField(default=1); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="assignments"); assigned_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="assignments_made"); assigned_at=models.DateTimeField(auto_now_add=True); due_at=models.DateTimeField(null=True,blank=True); is_mandatory=models.BooleanField(default=True); status=models.CharField(max_length=30,default="activa"); cancelled_at=models.DateTimeField(null=True,blank=True); cancellation_reason=models.TextField(blank=True); last_reminder_at=models.DateTimeField(null=True,blank=True)
    class Meta: constraints=[models.UniqueConstraint(fields=["course","user","course_version"],condition=models.Q(status="activa"),name="unique_active_assignment")]
class Enrollment(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="enrollments"); course_version=models.PositiveIntegerField(default=1); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="enrollments"); enrolled_at=models.DateTimeField(auto_now_add=True); enrollment_source=models.CharField(max_length=30,default="autoinscripcion"); status=models.CharField(max_length=30,default="activa")
    class Meta: unique_together=("course","user","course_version")
