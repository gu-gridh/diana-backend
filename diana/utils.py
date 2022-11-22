import json
from typing import *
from django.apps import apps
from django.urls import URLPattern, re_path
from diana.abstract import views
from rest_framework import serializers
from django.db import models

DEFAULT_FIELDS = ['created_at', 'updated_at', 'id']

DEFAULT_EXCLUDE = ['polymorphic_ctype']



def get_fields(model: models.Model, exclude: List[str] = DEFAULT_EXCLUDE) -> List[str]:
    """Utility to get the field/attribute/column names of a model. Includes many-to-many fields
    and has an optional exclude parameter to disallow custom parameters.

    Args:
        model (models.Model): A Django model
        exclude (List[str], optional): List of field names to exclude from the list. Defaults to DEFAULT_EXCLUDE.

    Returns:
        List[str]: A list of fields names as strings
    """
    return [field.name for field in (model._meta.fields + model._meta.many_to_many) if field.name not in exclude]


def get_many_to_many_fields(model: models.Model, exclude: List[str] = DEFAULT_EXCLUDE) -> List[str]:
    """Utility to get the many-to-many fields of a model. 

    Args:
        model (models.Model): A Django model
        exclude (List[str], optional): List of field names to exclude from the list. Defaults to DEFAULT_EXCLUDE.

    Returns:
        List[str]: A list of fields names as strings
    """
    return [field.name for field in (model._meta.many_to_many) if field.name not in exclude]


def read_json(path: str, encoding='utf-8', **kwargs) -> Dict:
    """Function to quickly read JSON files to a dictionary.

    Args:
        path (str): The absolute path of the JSON file
        encoding (str, optional): Optional string encoding. Defaults to 'utf-8'.

    Returns:
        Dict: The JSON file as a dictionary
    """


    with open(path, 'r', encoding=encoding) as f:
        return json.load(f, **kwargs)


def get_serializer(model: models.Model, fields: Callable[[models.Model], List[str]] = get_fields, depth: int = 0) -> serializers.ModelSerializer:
    """Generates a BaseSerializer class dynamically for a given model. This method avoids threading
    inconsistencies since the generated serialzer class always have different references.

    Args:
        model (models.Model): A Django model  
        fields (Callable[[models.Model], List[str]], optional): A function getting the field names of a model, yielding a list of strings. Defaults to get_fields.
        depth (int, optional): The nesting depth of foreign key models. Defaults to 0.

    Returns:
         serializers.ModelSerializer: A serializer class, not instance.
    """

    class DianaBaseSerializer(serializers.ModelSerializer):

        class Meta:
            model = None 

    DianaBaseSerializer.Meta.model = model
    DianaBaseSerializer.Meta.fields = fields(model)
    DianaBaseSerializer.Meta.depth  = depth
    DianaBaseSerializer.Meta.ref_name = model._meta.model_name

    return DianaBaseSerializer

def get_model_urls(app_label: str, base_url: str, exclude: List[str]) -> List[URLPattern]:
    """Dynamically generates Django URLPatterns with a basic view and serialization for models in a given app.

    Args:
        app_label (str): The app name 
        base_url (str): The base url endpoint for the model view
        exclude (List[str]): A list of model names to exclude

    Returns:
        List[URLPattern]: A list of URLPatterns to insert in the urls.py
    """

    # Fetch the application, with registered models
    app = apps.get_app_config(app_label)
    patterns = []

    # Create endpoint for each models, except the excluded ones
    for model_name, model in app.models.items():

        # Endpoints
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

