from django.db.models.fields.reverse_related import ManyToOneRel
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .fields import get_fields as fields

def default_view_set(model):
    """
    Dynamically define a REST view-set which uses the given model.
    """
    class ViewSet(viewsets.ModelViewSet):
        queryset = model.objects.all()
        serializer_class = _default_serializer(model)
        filterset_fields = _get_fields(model)
    return ViewSet



@api_view(['GET'])
def get_fields(request, project, tb):
    """
    Compile information about the models:
    - label
    - help text
    - type
    - relations
    - length of fields 
    """
    return Response(fields(project, tb))


def _default_serializer(model2):
    """
    Dynamically define a serializer which uses the given model.
    """
    class DefaultSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = model2
            fields = _get_fields(model)

    return DefaultSerializer

def _get_fields(model):
    """Get the names of the fields that will work for the REST view."""
    return [field.name for field in model._meta.get_fields() if _allow_field(field)]
    

def _allow_field(field):
    """Determine if a field works with the REST view."""
    # TODO: Make it so that relations can be used too.
    allow = not isinstance(field, ManyToOneRel)
    return allow # and not isinstance(field, ForeignKey)
