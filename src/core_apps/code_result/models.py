import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import URLValidator

from core_apps.common.models import TimeStampModel
from core_apps.code_display.models import Questions


class CodeExecutionResult(TimeStampModel):
    """Model to store the result of code execution from RCEE Service."""
    
    LANGUAGE_CHOICES = [
        ('py', 'Python'),
        ('cpp',  'C++'),  
        ('java',  'Java')
    ]

    question = models.ForeignKey(
        Questions,
        verbose_name=_("Original Question"),
        related_name="execution_results",  # Question.execution_results.all()
        on_delete=models.CASCADE,
    )

    user_id = models.UUIDField(verbose_name=_("User ID"))
    submission_id = models.UUIDField(verbose_name=_("Code Submission ID"))
    language = models.CharField(
        verbose_name=_("Programming Language"), default="py", max_length=25, choices=LANGUAGE_CHOICES
    )

    is_passed = models.BooleanField(
        verbose_name=_("Result of Code Execution"), default=False
    )

    # filled only if test cases failed.
    failed_test_case = models.CharField(
        verbose_name=_("Failed Test Cases"), max_length=255, blank=True
    )
    correct_output = models.CharField(
        verbose_name=_("Correct Output on the Test Case"), max_length=255, blank=True
    )
    user_output = models.CharField(
        verbose_name=_("User Output on the Test Case"), max_length=255, blank=True
    )

    s3_resource_link = models.TextField(
        verbose_name=_("S3 Resource Link"), validators=[URLValidator()]
    )

    def __str__(self) -> str:
        return f"The question: {self.question.title}, Submission ID: {self.submission_id} Executed at RCEE successfully."
