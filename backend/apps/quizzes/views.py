from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Quiz, Question, Attempt
from .serializers import QuizSerializer, QuestionSerializer, AttemptSerializer
from .services import grade_attempt
class QuizViewSet(viewsets.ModelViewSet):
    queryset=Quiz.objects.all(); serializer_class=QuizSerializer; permission_classes=[IsAuthenticated]; filterset_fields=["course","module","is_active"]
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_question(self, request, pk=None):
        # Builder del gestor: crea la pregunta con sus opciones en una sola llamada (is_correct solo se escribe, nunca se lee vía API de estudiante).
        from .models import Question, Option
        quiz = self.get_object()
        opts = request.data.get("options") or []
        if not opts: return Response({"detail": "La pregunta necesita opciones"}, status=400)
        q = Question.objects.create(quiz=quiz, question_type=request.data.get("question_type", "opcion_unica"), question_text=request.data.get("question_text", ""), points=request.data.get("points", 1), sort_order=request.data.get("sort_order", 0))
        for i, o in enumerate(opts):
            Option.objects.create(question=q, option_text=o.get("option_text", ""), is_correct=bool(o.get("is_correct")), sort_order=o.get("sort_order", i))
        from .serializers import QuestionSerializer
        return Response(QuestionSerializer(q).data, status=201)
class QuestionViewSet(viewsets.ModelViewSet):
    queryset=Question.objects.all(); serializer_class=QuestionSerializer; permission_classes=[IsAuthenticated]; filterset_fields=["quiz"]
class AttemptViewSet(viewsets.ModelViewSet):
    queryset=Attempt.objects.all(); serializer_class=AttemptSerializer; permission_classes=[IsAuthenticated]; filterset_fields=["quiz","user","passed"]
    def get_queryset(self):
        qs = super().get_queryset()
        u = self.request.user
        if u.is_superuser: return qs
        return qs.filter(user=u)
    def perform_create(self, serializer):
        from rest_framework.exceptions import ValidationError
        quiz = serializer.validated_data["quiz"]
        count = Attempt.objects.filter(quiz=quiz, user=self.request.user).count()
        if quiz.max_attempts and count >= quiz.max_attempts:
            raise ValidationError(f"Alcanzaste el máximo de intentos permitidos ({quiz.max_attempts}) para este quiz.")
        serializer.save(user=self.request.user, attempt_number=count + 1)
    @action(detail=True,methods=["post"])
    def answer(self,request,pk=None):
        from .models import Answer
        attempt=self.get_object()
        if attempt.submitted_at: return Response({"detail":"Intento ya enviado"},status=400)
        obj,_=Answer.objects.update_or_create(attempt=attempt,question_id=request.data.get("question"),defaults={"selected_option_id":request.data.get("selected_option"),"answer_text":request.data.get("answer_text","")})
        return Response({"ok":True,"answer_id":obj.id})
    @action(detail=True,methods=["post"])
    def submit(self,request,pk=None):
        attempt=self.get_object(); grade_attempt(attempt)
        try:
            if attempt.quiz and attempt.quiz.course:
                from apps.progress.services import recompute_course_progress
                recompute_course_progress(attempt.user, attempt.quiz.course)
        except Exception:
            pass
        return Response(AttemptSerializer(attempt).data)
