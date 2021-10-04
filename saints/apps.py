from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SaintsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saints'
    verbose_name = _("Saints")