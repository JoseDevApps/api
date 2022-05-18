from rest_framework import serializers
from .models import GD

class GDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GD
        fields = ['archivo', 'gd01', 'gd02']