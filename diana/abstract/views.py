from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from . import schemas


class AbstractViewSet(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    schema = schemas.MetaDataSchema()

    class Meta:
        abstract = True
