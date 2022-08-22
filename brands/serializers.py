from rest_framework import serializers
from brands.models import Brand


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'ko_name', 'en_name', 'url']
