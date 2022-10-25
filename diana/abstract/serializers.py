from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin

class GenericSerializer(serializers.ModelSerializer, DynamicFieldsMixin):

    class Meta:
        model = None
        fields = '__all__'
        depth = 1

class DynamicDepthSerializer(GenericSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.depth = self.context.get('depth', 0)

