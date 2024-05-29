from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CodeDisplayConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.code_display"
    verbose_name = _("Code Display")
    verbose_name_plural = _("Codes Display")
