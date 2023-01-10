from django.contrib import admin
from .admin_view import dict

def admin_view_site(apps_order):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)
        # a.sort(key=lambda x: b.index(x[0]))
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'])
        # Sort the models alphabetically within each app.
        for app in app_list:
            if app['name'] in apps_order:
                # app['models'] = apps_order[app['name']]
                app['models'].sort(key=lambda x: apps_order[app['name']].index(x['name']))
            else:
                app['models'].sort(key=lambda x: x['name'])

        return app_list
    return get_app_list

admin.AdminSite.get_app_list = admin_view_site(dict)
