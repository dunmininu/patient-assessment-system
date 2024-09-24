from django.db import models


class AssessmentType(models.TextChoices):
    COGNITIVE_STATUS = "Cognitive Status", "Cognitive Status"
    PHYSICAL_HEALTH = "Physical Health", "Physical Health"
    MENTAL_HEALTH = "Mental Health", "Mental Health"
    FUNCTIONAL_ABILITY = "Functional Ability", "Functional Ability"
    SOCIAL_SUPPORT = "Social Support", "Social Support"
