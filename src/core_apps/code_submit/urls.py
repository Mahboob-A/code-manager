from django.urls import path
from core_apps.code_submit.views import TestAPI, SubmitCode

urlpatterns = [
    path("test/", TestAPI.as_view()),
    path("submit/", SubmitCode.as_view(), name="submit_code"),
]
