from django.contrib import admin
from . import models


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lat', 'long')


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region')


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.StaticPage)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    prepopulated_fields = {
        'slug': ('title',)
    }