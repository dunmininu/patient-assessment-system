from rest_framework.routers import DefaultRouter
from .views import AssessmentViewSet, QuestionViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r"assessments", AssessmentViewSet)
router.register(r"questions", QuestionViewSet)
router.register(r"answers", AnswerViewSet)

urlpatterns = router.urls
