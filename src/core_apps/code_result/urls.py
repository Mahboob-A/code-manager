from django.urls import path

from core_apps.code_result.views import CodeExecutionResultAPI

urlpatterns = [
    path(
        "check/<submission_id>/",
        CodeExecutionResultAPI.as_view(),
        name="check_exec_result",
    ),
]
