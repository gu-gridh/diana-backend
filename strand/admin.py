"""
strand.admin and saints.admin is exactly the same except for the name
of the app. Should be refactored somehow.

Of course, make sure to make all changes to both files until
refactoring is done.
"""
from django.apps import apps
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

project = 'strand'

all_models = apps.get_app_config(project).get_models()

class AdminSite(admin.AdminSite):
    site_header = _("admin_portal")
    site_title = _("admin_portal")
    index_title = _("admin_index")

admin_site = AdminSite(name=project)


admin_site.register(all_models)
