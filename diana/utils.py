import json
from typing import *
from django.apps import apps
from django.urls import re_path
from diana.abstract import serializers, views

def read_json(path: str) -> Dict:

    with open(path, 'r') as f:
        return json.load(f)


def get_serializer(model):

    serializer = serializers.GenericSerializer
    serializer.Meta.model = model

    return serializer

def get_model_urls(app_label: str, base_url: str, exclude: List[str]):

    # Fetch the application, with registered models
    app = apps.get_app_config(app_label)
    patterns = []

    for model_name, model in app.models.items():

        urls = {
            'list': rf'{base_url}/{model_name}/?$',
            'retrieve': rf'{base_url}/{model_name}/<int:pk>/?$',
            'count': rf'{base_url}/{model_name}/count/?$',
        }

        for action, url in urls.items():

            if model_name not in exclude:
                
                patterns.append(
                    re_path(
                        url, 
                        views.GenericModelViewSet.as_view(actions={'get': action}, 
                        queryset=model.objects.all(), 
                        serializer_class=get_serializer(model)), 
                        {'model': model}
                        )
                    )

    return patterns

