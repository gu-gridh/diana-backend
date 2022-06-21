import json
from typing import *
from django.apps import apps
from django.urls import re_path
from diana.abstract import views
from rest_framework import serializers
from django.db import models
DEFAULT_EXCLUDE = ['created_at', 'updated_at', 'published', 'polymorphic_ctype']



def get_fields(model: models.Model, exclude=DEFAULT_EXCLUDE):
    return [field.name for field in (model._meta.fields + model._meta.many_to_many) if field.name not in exclude]


def read_json(path: str) -> Dict:

    with open(path, 'r') as f:
        return json.load(f)


def get_serializer(model):

    class BaseSerializer(serializers.ModelSerializer):

        class Meta:
            model = None 

    BaseSerializer.Meta.model = model
    BaseSerializer.Meta.fields = get_fields(model)
    BaseSerializer.Meta.depth  = 1

    return BaseSerializer

def get_model_urls(app_label: str, base_url: str, exclude: List[str]):

    # Fetch the application, with registered models
    app = apps.get_app_config(app_label)
    patterns = []

    for model_name, model in app.models.items():

        urls = {
            'list': rf'{base_url}/{model_name}/?$',
            'retrieve': rf'{base_url}/{model_name}/(?P<pk>[0-9]+)/',
            'count': rf'{base_url}/{model_name}/count/?$',
        }

        for action, url in urls.items():

            if model_name not in exclude:
                
                patterns.append(
                    re_path(
                        url, 
                        views.GenericModelViewSet.as_view({'get': action}, 
                        queryset=model.objects.all(), 
                        serializer_class=get_serializer(model)), 
                        {'model': model}
                        )
                    )

    return patterns

