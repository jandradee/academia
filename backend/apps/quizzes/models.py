from django.db import models
from django.conf import settings
class Quiz(models.Model):
    course=models.ForeignKey("courses.Course",on_delete=models.CASCADE,related_name="quizzes",null=True,blank=True); module=models.ForeignKey("courses.Module",on_delete=models.CASCADE,related_name="quizzes",null=True,blank=True); title=models.CharField(max_length=255); instructions=models.TextField(blank=True); pass_score=models.DecimalField(max_digits=5,decimal_places=2,default=70); max_attempts=models.PositiveIntegerField(null=True,blank=True); time_limit_seconds=models.PositiveIntegerField(null=True,blank=True); is_active=models.BooleanField(default=True); version=models.PositiveIntegerField(default=1)
class Question(models.Model):
    class T(models.TextChoices): SINGLE="opcion_unica","Opción única"; MULTI="seleccion_multiple","Selección múltiple"; TF="verdadero_falso","Verdadero/Falso"; SHORT="respuesta_corta","Respuesta corta"
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="questions"); question_type=models.CharField(max_length=30,choices=T.choices,default=T.SINGLE); question_text=models.TextField(); points=models.DecimalField(max_digits=6,decimal_places=2,default=1); sort_order=models.IntegerField(default=0); is_required=models.BooleanField(default=True)
    class Meta: ordering=["sort_order"]
class Option(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name="options"); option_text=models.CharField(max_length=500); is_correct=models.BooleanField(default=False); sort_order=models.IntegerField(default=0)
class Attempt(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE,related_name="attempts"); user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="quiz_attempts"); started_at=models.DateTimeField(auto_now_add=True); submitted_at=models.DateTimeField(null=True,blank=True); score=models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True); passed=models.BooleanField(null=True,blank=True); attempt_number=models.PositiveIntegerField(default=1); duration_seconds=models.PositiveIntegerField(null=True,blank=True)
class Answer(models.Model):
    attempt=models.ForeignKey(Attempt,on_delete=models.CASCADE,related_name="answers"); question=models.ForeignKey(Question,on_delete=models.CASCADE); selected_option=models.ForeignKey(Option,on_delete=models.SET_NULL,null=True,blank=True); answer_text=models.TextField(blank=True); points_awarded=models.DecimalField(max_digits=6,decimal_places=2,default=0)
