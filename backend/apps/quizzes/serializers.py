from rest_framework import serializers
from .models import Quiz, Question, Option, Attempt, Answer
class OptionSerializer(serializers.ModelSerializer):
    class Meta: model=Option; fields=["id","option_text","sort_order"]  # nunca exponer is_correct al colaborador
class OptionAdminSerializer(serializers.ModelSerializer):
    class Meta: model=Option; fields="__all__"
class QuestionSerializer(serializers.ModelSerializer):
    options=OptionSerializer(many=True,read_only=True)
    class Meta: model=Question; fields=["id","quiz","question_type","question_text","points","sort_order","is_required","options"]
class QuizSerializer(serializers.ModelSerializer):
    questions=QuestionSerializer(many=True,read_only=True)
    class Meta: model=Quiz; fields="__all__"
class AttemptSerializer(serializers.ModelSerializer):
    class Meta: model=Attempt; fields="__all__"; read_only_fields=["score","passed","submitted_at","user","attempt_number"]
class AnswerSerializer(serializers.ModelSerializer):
    class Meta: model=Answer; fields="__all__"
