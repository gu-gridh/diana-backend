from rest_framework import viewsets, generics, mixins, pagination
from django_filters.rest_framework import DjangoFilterBackend
from . import schemas, serializers


from rest_framework.decorators import action
from rest_framework.response import Response

class CountModelMixin(object):
    """
    Count a queryset.
    """
    @action(detail=False)
    def count(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        content = {'count': queryset.count()}
        return Response(content)


class GenericPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class GenericModelViewSet(viewsets.ModelViewSet, CountModelMixin):

    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    pagination_class = GenericPagination
    schema = schemas.AutoSchema()
