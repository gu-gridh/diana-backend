from django.contrib.gis import admin
from django.utils.translation import gettext_lazy as _
from diana.utils import get_fields, DEFAULT_FIELDS, DEFAULT_EXCLUDE

class AbstractModelAdmin(admin.ModelAdmin):

    readonly_fields = [*DEFAULT_FIELDS]

class AbstractImageModelAdmin(admin.ModelAdmin):

    pass