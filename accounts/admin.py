from django.contrib import admin
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('guid', 'is_staff', 'is_active', 'username', 'phone_number', 'product', 'category')
    readonly_fields = ('last_login', 'date_joined')