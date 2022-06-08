from rest_framework import viewsets, generics, mixins
from django_filters.rest_framework import DjangoFilterBackend
from . import schemas, serializers

class GenericReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):

    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    schema  = schemas.MetaDataSchema()