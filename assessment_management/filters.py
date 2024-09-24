from django_filters import rest_framework as filters

from assessment_management.models import Assessment


class AssessmentFilter(filters.FilterSet):
    assessment_type = filters.CharFilter(
        field_name="assessment_type", lookup_expr="icontains"
    )
    assessment_date = filters.DateFilter(field_name="assessment_date")
    patient_id = filters.NumberFilter(field_name="patient__id")

    class Meta:
        model = Assessment
        fields = ["assessment_type", "assessment_date", "patient_id"]
