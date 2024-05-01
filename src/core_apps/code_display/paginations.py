from rest_framework.pagination import PageNumberPagination


class QuestionPageNumberPagination(PageNumberPagination):
    """Pagination class for core_apps.code_display.models.Questions"""

    page_size = 10
    page_size_query_param = "page"
    max_page_size = 25
