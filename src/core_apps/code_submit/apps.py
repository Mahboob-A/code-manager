from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CodeSubmitConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.code_submit"
    verbose_name = _("Code Submit")
    verbose_name_plural = _("Code Submits")
