from collections import OrderedDict, defaultdict
from rest_framework.fields import SkipField
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from . import models
from rest_framework.relations import PKOnlyObject
from django.db import connection
class MetaObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Object
        fields = '__all__'
        depth = 1

class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Object
        fields = '__all__'
        depth = 1


class ParishSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Parish
        fields = '__all__'
        depth = 1

class PlaceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = models.Place
        fields = '__all__'
        geo_field = 'geom'

class MotiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Motive
        fields = '__all__'
        depth = 1

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'