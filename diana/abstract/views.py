from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_gis.filters import InBBoxFilter
from rest_framework_gis.pagination import GeoJsonPagination


from . import schemas

class CountModelMixin(object):
    """
    Creates an additional action/endpoint counting the objects 
    for the specific filtering query, avoiding any fetch of objects.
    """
    @action(detail=False)
    def count(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        content = {'count': queryset.count()}
        return Response(content)

class GenericPagination(pagination.LimitOffsetPagination):
    """
    The pagination of choice is limit-offset pagination.
    """
    default_limit = 25

class GeoJsonPagePagination(GeoJsonPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20

class GenericModelViewSet(viewsets.ModelViewSet, CountModelMixin):
    """
    The GenericModelViewSet allows the creation of a a model agnostic model view
    with elementary filtering support and pagination.
    """
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    pagination_class = GenericPagination
    schema = schemas.AutoSchema()


class DynamicDepthViewSet(GenericModelViewSet):

    def get_serializer_context(self):
        context = super().get_serializer_context()
        depth = 0
        try:
            depth = int(self.request.query_params.get('depth', 0))
            print(depth)
        except ValueError:
            pass # Ignore non-numeric parameters and keep default 0 depth
        
        context['depth'] = depth

        return context

class GeoViewSet(GenericModelViewSet):

    filter_backends = [InBBoxFilter, DjangoFilterBackend]
    schema = schemas.AutoSchema()
    
    # GIS filters
    # Default field name
    bbox_filter_field = 'geometry'

    # Specialized pagination
    pagination_class = GeoJsonPagePagination
    page_size = 10