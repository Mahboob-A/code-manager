from django_filters import FilterSet, filters

from core_apps.code_display.models import Questions


class QuestionFilter(FilterSet):
    """'Filter class for core_apps.code_display.models.Questions model"""

    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    tags = filters.CharFilter(field_name="tags__name", lookup_expr="icontains")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    updated_at = filters.DateFromToRangeFilter(field_name="updated_at")

    class Meta:
        model = Questions
        fields = ["title", "tags", "created_at", "updated_at"]

