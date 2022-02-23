from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis.filters import GeometryFilter
from django_filters import filters
from . import models

# class PlaceFilter(GeoFilterSet):
#     contains_geom = GeometryFilter(name='geom', lookup_expr='equals')

#     class Meta:
#         model = models.Place
#         fields = ['geom']