dict = {}


def get_apps_order(app_label, models_order):
    global dict
    dict[app_label] = models_order
