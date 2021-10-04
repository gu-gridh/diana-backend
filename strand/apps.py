from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StrandConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'strand'
    verbose_name = _("strand")
