from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CodeResultConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.code_result"
    verbose_name = _("Code Result")
    verbose_name_plural = _("Code Results")
