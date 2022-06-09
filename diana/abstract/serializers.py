from rest_framework import serializers

class GenericSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = '__all__'
        depth = 1