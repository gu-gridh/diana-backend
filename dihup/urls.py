"""dihup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path, include
from django.apps import apps

from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from strand.admin import admin_site as strand_admin_site
from saints.admin import admin_site as saints_admin_site
from .views import get_fields, default_view_set


# Customizing Admin page with translatable (_) strings
admin.site.index_title = _("admin_index")
admin.site.site_header = _("admin_portal")
admin.site.site_title = _("admin_portal")

urlpatterns = []

for project in ["saints", "strand"]:
    router = routers.DefaultRouter()
    models = apps.get_app_config(project).get_models()
    for model in models:
        router.register(model._meta.model_name, default_view_set(model))

    urlpatterns.append(path(project + "/", include(router.urls)))

    

urlpatterns.extend([
    path('admin/', admin.site.urls),
    path('strand-admin/', strand_admin_site.urls),
    path('saints-admin/', saints_admin_site.urls),
    # allows ?format=<json/xml>
    # urlpatterns = format_suffix_patterns(urlpatterns)
    # must add format=None on view
    path('<project>/fields/<tb>', get_fields)
])

# i18n_patterns is used to automatically prefix /sv/, /fi/, /da/ or whatever to
# the URLs. prefix_default_language=False does not add a prefix to the default
# language. (LANGUAGE_CODE in settings)
urlpatterns = i18n_patterns(*urlpatterns, prefix_default_language=False)