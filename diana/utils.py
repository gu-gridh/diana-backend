import json
from typing import *
from django.apps import apps

from diana.abstract import serializers, views

def read_json(path: str) -> Dict:

    with open(path, 'r') as f:
        return json.load(f)

def get_read_only_urls(app_label: str, base_url: str, exclude: List[str]):

    # Fetch the application, with registered models
    app = apps.get_app_config(app_label)

    url_configs = []

    for model_name, model in app.models.items():

        # Get the url of the specific model
        url = rf'{base_url}/{model_name}'

        if model_name not in exclude:
            
            # Add a viewset
            viewset = views.GenericReadOnlyModelViewSet
            viewset.queryset = model.objects.all()

            # Add a basic serializer
            serializer = serializers.GenericSerializer
            serializer.Meta.model = model

            viewset.serializer_class = serializer
            
            url_configs.append({'prefix': url, 'viewset': viewset, 'basename': model_name})

    return url_configs