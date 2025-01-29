from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts.serializers import UserForGetSerializer
from common.serializers import AddressSerializer
from . import models
from accounts.models import User


class ChildrenCategorySerializer(serializers.ModelSerializer):
    ads_count = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'ads_count', 'children')

    def get_ads_count(self, obj):
        return obj.ads_count()

    def get_children(self, obj):
        if obj.children.exists():
            return ChildrenCategorySerializer(obj.children, many=True).data
        return []

class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False, allow_null=True)
    ads_count = serializers.SerializerMethodField()
    children = ChildrenCategorySerializer(read_only=True, many=True)

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'ads_count', 'icon', 'children')

    def to_representation(self, instance):
        if instance.parent:
            return None
        representation = super().to_representation(instance)
        return representation

    def get_ads_count(self, obj):
        return obj.ads_count()


class ParentCategorySerializer(serializers.ModelSerializer):
    ads_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ("id", "name", "ads_count", "icon")

    def get_ads_count(self, obj):
        return obj.ads_count()


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = ("id", "name", "category")

    def get_category(self, obj):
        if obj.parent.exists():
            return ParentCategorySerializer(read_only=True, many=True).data
        return None


class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('id', 'is_mine', 'status', 'expires_at')


class ProductForGetSerializer(serializers.ModelSerializer):
    images = serializers.ImageField(required=False, allow_null=True)
    sub_category = SubCategorySerializer(source='category', read_only=True)
    extra = ExtraSerializer(read_only=True)

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'slug', 'sub_category', 'images', 'price', 'currency', 'published_at', 'updated_at', 'description', 'phone_number', 'address', 'seller', 'extra')


    def to_representation(self, instance):
        if not instance.validate_extra():
            return None
        representation = super().to_representation(instance)
        representation['address'] = AddressSerializer(instance.validate_address).data
        representation['seller'] = UserForGetSerializer(instance.seller).data
        return representation


class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    images = serializers.ImageField(required=False, allow_null=True)
    sub_category = SubCategorySerializer(source='category', read_only=True)
    extra = ExtraSerializer(read_only=True, required=False, allow_null=True)

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'slug', 'sub_category', 'author', 'images', 'price', 'currency', 'published_at', 'updated_at', 'description', 'phone_number', 'address', 'seller', 'extra')


    def create(self, validated_data):
        images = validated_data.pop('images', None)
        product = models.Product.objects.create(seller=self.context['request'].user, **validated_data)

        if images:
            if isinstance(images, list):
                for image in images:
                    if not isinstance(image, (InMemoryUploadedFile, TemporaryUploadedFile)):
                        raise ValidationError("Each image must be a valid file object.")
                    photo = models.Image.objects.create(image=image, product=product)
                    photo.save()
            elif isinstance(images, (InMemoryUploadedFile, TemporaryUploadedFile)):
                photo = models.Image.objects.create(image=images, product=product)
                photo.save()

        return product


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PopularSearchWord
        fields = ('id', 'word', 'count')