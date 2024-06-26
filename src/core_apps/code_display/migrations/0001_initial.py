# Generated by Django 4.2.11 on 2024-05-07 14:51

import autoslug.fields
from django.db import migrations, models
import taggit.managers
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
    ]

    operations = [
        migrations.CreateModel(
            name="Companies",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Question Title"),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Company Description"
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Questions",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Question Title"),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        always_update=True,
                        editable=False,
                        populate_from="title",
                        unique=True,
                    ),
                ),
                (
                    "difficulty",
                    models.IntegerField(
                        choices=[
                            (1, "Easy"),
                            (2, "Medium"),
                            (3, "Hard"),
                            (4, "Master"),
                            (5, "Grand Master"),
                        ],
                        verbose_name="Question Difficulty",
                    ),
                ),
                (
                    "acceptance_rate",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                ("description", models.TextField(verbose_name="Questions Description")),
                (
                    "testcases_inputs",
                    models.TextField(verbose_name="Complete Test Cases"),
                ),
                (
                    "testcases_answers",
                    models.TextField(verbose_name="Complete Test Cases Answers"),
                ),
                (
                    "testcases_example",
                    models.TextField(
                        max_length=2000, verbose_name="A Few Test Case Examples"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        default="Questions/Images/dsa.png",
                        upload_to="Questions/Images",
                        verbose_name="Related Imgae to the Question",
                    ),
                ),
                (
                    "constraints",
                    models.TextField(
                        max_length=1000, verbose_name="Question Constraints"
                    ),
                ),
                (
                    "companies",
                    models.ManyToManyField(
                        blank=True,
                        related_name="questions",
                        to="code_display.companies",
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
            options={
                "verbose_name": "Question",
                "verbose_name_plural": "Questions",
                "ordering": ["-created_at"],
            },
        ),
    ]
