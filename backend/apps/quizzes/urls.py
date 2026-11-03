from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuestionViewSet, AttemptViewSet
router=DefaultRouter(); router.register("quizzes",QuizViewSet); router.register("questions",QuestionViewSet); router.register("quiz-attempts",AttemptViewSet)
urlpatterns=router.urls
