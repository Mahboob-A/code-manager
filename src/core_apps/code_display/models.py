from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from core_apps.common.models import TimeStampModel


class Companies(TimeStampModel):
    """Company names to map the questions by companies"""

    title = models.CharField(verbose_name=_("Company Title"), max_length=255)
    description = models.CharField(
        verbose_name=_("Company Description"), max_length=255, blank=True
    )

    def __str__(self) -> str:
        return f"Company: {self.title}"


class Questions(TimeStampModel):
    """Question/Problem List Model for AlgoCode"""

    DIFFICULTY_CHOICES = (
        (1, "Easy"),
        (2, "Medium"),
        (3, "Hard"),
        (4, "Master"),
        (5, "Grand Master"),
    )

    title = models.CharField(verbose_name=_("Question Title"), max_length=255)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    companies = models.ManyToManyField(Companies, related_name="questions", blank=True)
    difficulty = models.IntegerField(
        verbose_name=_("Question Difficulty"), choices=DIFFICULTY_CHOICES
    )
    acceptance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    # deccriptions and test cases
    description = models.TextField(verbose_name=_("Questions Description"))
    testcases_inputs = models.TextField(verbose_name=_("Complete Test Cases"))
    testcases_answers = models.TextField(verbose_name=_("Complete Test Cases Answers"))

    # test case examples and constraints
    testcases_example = models.TextField(
        verbose_name=_("A Few Test Case Examples"), max_length=2000
    )
    image = models.ImageField(
        verbose_name=_("Related Imgae to the Question"),
        upload_to="Questions/Images",
        default="Questions/Images/dsa.png",
    )
    constraints = models.TextField(
        verbose_name=_("Question Constraints"), max_length=1000
    )

    # question tags (ex: array, linked_list, string, queue, stack etc.)
    tags = TaggableManager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Question: {self.title}"
