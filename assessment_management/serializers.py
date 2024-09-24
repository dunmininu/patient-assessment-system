from rest_framework import serializers
from .models import Question, Answer, Assessment


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text", "assessment_type"]


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["text", "assessment_type"]

    def create(self, validated_data):
        user = self.context["request"].user
        tenant = getattr(user, "tenant", None)

        if tenant is None:
            raise serializers.ValidationError("User must be associated with a tenant.")

        validated_data["tenant"] = tenant
        return super().create(validated_data)

    def to_representation(self, instance):
        return QuestionSerializer(instance).data


class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = ["id", "question", "text", "score"]


class AnswerCreateSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(), source="question"
    )

    class Meta:
        model = Answer
        fields = ["question_id", "assessment", "text", "score"]

    def create(self, validated_data):
        user = self.context["request"].user
        tenant = getattr(user, "tenant", None)

        if tenant is None:
            raise serializers.ValidationError("User must be associated with a tenant.")

        validated_data["tenant"] = tenant
        return super().create(validated_data)

    def to_representation(self, instance):
        return AnswerSerializer(instance).data


class AssessmentSerializer(serializers.ModelSerializer):
    patient_full_name = serializers.ReadOnlyField(source="patient.full_name")

    class Meta:
        model = Assessment
        fields = [
            "id",
            "assessment_type",
            "patient",
            "patient_full_name",
            "assessment_date",
            "final_score",
            "created_at",
            "updated_at",
        ]


class AssessmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ["assessment_type", "patient", "assessment_date"]

    def create(self, validated_data):
        user = self.context["request"].user

        tenant = getattr(user, "tenant", None)

        if tenant is None:
            raise serializers.ValidationError("User must be associated with a tenant.")

        validated_data["created_by"] = user
        validated_data["tenant"] = tenant

        return super().create(validated_data)

    def to_representation(self, instance):
        return AssessmentSerializer(instance).data
