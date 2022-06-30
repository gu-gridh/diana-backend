from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, pagination
from rest_framework.decorators import action
from rest_framework.response import Response

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

class GenericModelViewSet(viewsets.ModelViewSet, CountModelMixin):
    """
    The GenericModelViewSet allows the creation of a a model agnostic model view
    with elementary filtering support and pagination.
    """
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    pagination_class = GenericPagination
    schema = schemas.AutoSchema()
