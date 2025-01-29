from rest_framework import serializers
from . import models


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ('id', 'name')


class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = models.District
        fields = ('id', 'name', 'region')


class RegionListSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(read_only=True, many=True)

    class Meta:
        model = models.Region
        fields = ('id', 'name', 'districts')


class AddressSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)

    class Meta:
        model = models.Address
        fields = ('id', 'district', 'name', 'lat', 'long')

class StaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaticPage
        fields = ('id', 'title', 'slug', 'created_at', 'updated_at', 'description')