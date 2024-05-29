from django.urls import path

from core_apps.code_submit.views import SubmitCode

urlpatterns = [
    path("submit/", SubmitCode.as_view(), name="submit_code"),
]
