from rest_framework import serializers
from . import models
from products.models import Category
from common.serializers import AddressSerializer



class UserForGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id','guid', 'username', 'password', 'product', 'phone_number', 'category', 'address', 'profile_photo')


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['address'] = AddressSerializer(instance.validate_address).data
        from products.serializers import CategorySerializer
        representation['category'] = CategorySerializer(instance.category).data
        return representation


class UserForCreateUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    username = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = models.User
        fields = ('id','guid', 'username', 'product', 'phone_number', 'category', 'address', 'profile_photo')


    def create(self, validated_data):
        user = models.User.objects.create(**validated_data)
        user.is_active = False
        user.save()
        return user