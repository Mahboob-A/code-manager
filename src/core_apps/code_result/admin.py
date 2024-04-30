from django.contrib import admin


from core_apps.code_result.models import CodeExecutionResult


@admin.register(CodeExecutionResult)
class CodeExecutionResultAdmin(admin.ModelAdmin):
    """Model Admin class for CodeExecutionResult"""

    list_display = ["id", "pkid", "question", "is_passed", "submission_id"]
    list_display_links = ["id", "pkid", "question"]
    list_filter = ["created_at", "updated_at"]
    search_fields = [
        "is_passed",
        "submission_id",
        "question__tags__name",
        "question__companies__title",
    ]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Code Identification",
            {"fields": ["user_id", "submission_id", "question"]},
        ),
        (
            "Code Execution Result",
            {
                "fields": [
                    "language",
                    "is_passed",
                    "failed_test_case",
                    "correct_output",
                    "user_output",
                ]
            },
        ),
        ("Resources", {"fields": ["s3_resource_link"]}),
    )
