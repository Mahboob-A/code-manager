from django.contrib import admin

from core_apps.code_display.models import Questions, Companies


@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "title", "description"]
    list_display_links = ["id", "pkid", "title"]


@admin.register(Questions)
class QuestionAdmin(admin.ModelAdmin):
    """Admin class for Question model."""

    list_display = ["id", "pkid", "title", "difficulty", "slug"]
    list_display_links = ["pkid", "id", "title"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["title", "description", "tags__name", "companies"]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"
    fieldsets = [
        (
            "Question Information",
            {
                "fields": [
                    "title",
                ]
            },
        ),
        (
            "Question Content",
            {
                "fields": [
                    "description",
                    "acceptance_rate",
                    "difficulty",
                    "image",
                ]
            },
        ),
        (
            "Question Test Cases and Constraints",
            {
                "fields": [
                    "testcases_example",
                    "testcases_inputs",
                    "testcases_answers",
                    "constraints",
                ]
            },
        ),
        ("Tags and Companies", {"fields": ["tags", "companies"]}),
    ]
