from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis.filters import InBBoxFilter
from rest_framework_gis.pagination import GeoJsonPagination

from . import models, serializers, filters
from rest_framework.decorators import action
from rest_framework.response import Response

class ObjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Object.objects.all()
    serializer_class = serializers.ObjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

class ParishViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Parish.objects.all()
    serializer_class = serializers.ParishSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Place.objects.all()
    serializer_class = serializers.PlaceSerializer
    filter_backends = [InBBoxFilter, DjangoFilterBackend]
    
    # GIS filters
    bbox_filter_field = 'geom'
    # bbox_filter_include_overlapping = True # Optional

    # Generic filters
    filterset_fields = models.get_fields(models.Place, exclude=['id', 'geom'])

    # Specialized pagination
    pagination_class = GeoJsonPagination


class MotiveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Motive.objects.all()
    serializer_class = serializers.MotiveSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Image.objects.all()
    serializer_class = serializers.MotiveSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


# @action(methods=['GET'], detail=False)
# def api_schema(self, request):
#     meta = self.metadata_class()
#     data = meta.determine_metadata(request, self)
#     return Response(data)