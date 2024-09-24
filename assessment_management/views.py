from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters

from assessment_management.filters import AssessmentFilter
from users.permissions import IsAdmin, IsTenantUser
from .models import Question, Answer, Assessment
from .serializers import (
    QuestionSerializer,
    QuestionCreateSerializer,
    AnswerSerializer,
    AnswerCreateSerializer,
    AssessmentSerializer,
    AssessmentCreateSerializer,
)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = [IsTenantUser | IsAdmin]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return QuestionCreateSerializer
        return QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    permission_classes = [IsTenantUser | IsAdmin]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return AnswerCreateSerializer
        return AnswerSerializer


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    permission_classes = [IsTenantUser | IsAdmin]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AssessmentFilter

    def get_serializer_class(self):
        if self.action in ["create"]:
            return AssessmentCreateSerializer
        return AssessmentSerializer
