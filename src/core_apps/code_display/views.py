# python
import logging

from django.http import Http404

# django
from django.shortcuts import get_object_or_404, render

# django filters
from django_filters.rest_framework import DjangoFilterBackend

# drf
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core_apps.code_display.filters import QuestionFilter

# locals
from core_apps.code_display.models import Questions
from core_apps.code_display.paginations import QuestionPageNumberPagination
from core_apps.code_display.renderers import QuestionJSONRenderer, QuestionsJSONRenderer
from core_apps.code_display.serializers import QuestionGETSerializer

logger = logging.getLogger(__name__)


class QuestionListAPIView(generics.ListAPIView):
    """API for Question List View"""

    queryset = Questions.objects.all()
    serializer_class = QuestionGETSerializer
    filterset_class = QuestionFilter
    pagination_class = QuestionPageNumberPagination

    permission_classes = [AllowAny]
    renderer_classes = [QuestionsJSONRenderer]
    ordering_fields = ["-created_at", "-updated_at"]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]


class QuestionDetailAPIView(generics.RetrieveAPIView):
    """API for a singel Question retrival"""

    queryset = Questions.objects.all()
    serializer_class = QuestionGETSerializer
    permission_classes = [AllowAny]
    renderer_classes = [QuestionJSONRenderer]

    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            questioin_id = self.kwargs.get("id")
            logger.warning(f"[x]: Question with id: {questioin_id} does not found.")
            return Response(
                {"detail": "Question does not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
