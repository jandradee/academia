from decimal import Decimal
from django.utils import timezone
from .models import Attempt, Answer, Option
def grade_attempt(attempt):
    # Calificación 100% en servidor (RF-008): nunca confiar en puntaje del cliente.
    total=Decimal("0"); earned=Decimal("0")
    for q in attempt.quiz.questions.all():
        total+=q.points
        ans=Answer.objects.filter(attempt=attempt,question=q).first()
        if ans and ans.selected_option and ans.selected_option.is_correct:
            ans.points_awarded=q.points; earned+=q.points
        elif ans: ans.points_awarded=Decimal("0")
        if ans: ans.save()
    score=(earned/total*100) if total else Decimal("0")
    attempt.score=score; attempt.passed=score>=attempt.quiz.pass_score; attempt.submitted_at=timezone.now(); attempt.save()
    return attempt
