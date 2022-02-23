from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'api/object', views.ObjectViewSet, basename='object')
router.register(r'api/place', views.PlaceViewSet, basename='place')
router.register(r'api/parish', views.ParishViewSet, basename='parish')
router.register(r'api/image', views.ImageViewSet, basename='image')
router.register(r'api/motive', views.MotiveViewSet, basename='motive')
urlpatterns = [
    path('', include(router.urls)),
]