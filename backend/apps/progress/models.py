from django.db import models
from django.conf import settings
class CourseProgress(models.Model):
    class S(models.TextChoices): NOT_STARTED="no_iniciado","No iniciado"; IN_PROGRESS="en_progreso","En progreso"; COMPLETED="completado","Completado"; PASSED="aprobado","Aprobado"; EXPIRED="vencido","Vencido"; CANCELLED="cancelado","Cancelado"
    course=models.ForeignKey("courses.Course",on_delete=models.CASCADE,related_name="progress"); course_version=models.PositiveIntegerField(default=1); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="course_progress"); status=models.CharField(max_length=20,choices=S.choices,default=S.NOT_STARTED); progress_percent=models.DecimalField(max_digits=5,decimal_places=2,default=0); first_started_at=models.DateTimeField(null=True,blank=True); last_activity_at=models.DateTimeField(null=True,blank=True); completed_at=models.DateTimeField(null=True,blank=True); passed_at=models.DateTimeField(null=True,blank=True)
    class Meta: unique_together=("course","user","course_version")
class ModuleProgress(models.Model):
    module=models.ForeignKey("courses.Module",on_delete=models.CASCADE,related_name="progress"); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE); status=models.CharField(max_length=20,default="pendiente"); progress_percent=models.DecimalField(max_digits=5,decimal_places=2,default=0); started_at=models.DateTimeField(null=True,blank=True); completed_at=models.DateTimeField(null=True,blank=True)
    class Meta: unique_together=("module","user")
class VideoProgress(models.Model):
    video=models.ForeignKey("courses.Video",on_delete=models.CASCADE,related_name="progress"); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE); last_position_seconds=models.PositiveIntegerField(default=0); max_position_seconds=models.PositiveIntegerField(default=0); completed_at=models.DateTimeField(null=True,blank=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: unique_together=("video","user")
    @property
    def percent(self):
        return (self.max_position_seconds/self.video.duration_seconds*100) if self.video.duration_seconds else 0

class ResourceProgress(models.Model):
    resource=models.ForeignKey("courses.Resource",on_delete=models.CASCADE,related_name="progress"); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE); viewed_at=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=("resource","user")
