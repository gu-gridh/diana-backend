from django.urls import path, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

from . import views

router = routers.DefaultRouter()

router.register(r'api/object', views.ObjectViewSet, basename='object')
router.register(r'api/place', views.PlaceViewSet, basename='place')
router.register(r'api/parish', views.ParishViewSet, basename='parish')
router.register(r'api/image', views.ImageViewSet, basename='image')
router.register(r'api/motive', views.MotiveViewSet, basename='motive')
urlpatterns = [
    path('', include(router.urls)),
    path('api/schema', get_schema_view(
        title="Iconographia",
        description="Schema for the Iconographia API at the Centre for Digital Humanities",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('redoc-ui/', TemplateView.as_view(
        template_name='redoc-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc-ui'),
]