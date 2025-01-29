from django.contrib import admin
from . import models


class ImageInLine(admin.TabularInline):
    model = models.Image
    extra = 1
    raw_id_fields = ('product',)


class CategoryInLine(admin.TabularInline):
    model = models.Category
    extra = 1
    raw_id_fields = ('parent',)


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'product')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'name')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'currency', 'seller')
    prepopulated_fields = {
        'slug': ('name',)
    }
    inlines = [ImageInLine]



