from django.db import models

from assessment_management.choices import AssessmentType
from users.models import Tenant, User
from patient_management.models import Patient


class Question(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="tenant_questions"
    )
    text = models.CharField(max_length=255)
    assessment_type = models.CharField(max_length=50)

    def __str__(self):
        return self.text


class Answer(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="tenant_answers"
    )
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    assessment = models.ForeignKey(
        "Assessment", related_name="assessment_answers", on_delete=models.CASCADE
    )
    text = models.TextField()
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Answer to {self.question.text}: {self.text}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.assessment.calculate_final_score()


class Assessment(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="patients"
    )

    assessment_type = models.CharField(
        max_length=50,
        choices=AssessmentType.choices,
        default=AssessmentType.COGNITIVE_STATUS,
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient_assessment"
    )
    assessment_date = models.DateField()
    final_score = models.FloatField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assessments"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assessment_type} for {self.patient.full_name}"

    def calculate_final_score(self):
        # Get all the answers related to this assessment
        answers = self.assessment_answers.all()

        # Calculate the average score if there are any answers with non-null scores
        if answers.exists():
            average_score = answers.aggregate(models.Avg("score"))["score__avg"]
            self.final_score = average_score
            self.save()
        else:
            self.final_score = None
            self.save()
