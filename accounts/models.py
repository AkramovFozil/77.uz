import uuid
from django.core.validators import RegexValidator
from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        Seller = "seller", _("Seller")
        Admin = "admin", _("Admin")

    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    username = models.CharField(_("full username"), max_length=150, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, null=True)
    product = models.CharField(max_length=250)
    address = models.CharField(max_length=255)
    validate_address = models.ForeignKey("common.Address", on_delete=models.SET_NULL, related_name="users", null=True,
                                         blank=True)
    profile_photo = models.ImageField(upload_to="profile_image/", blank=True, null=True)
    phone_number = models.CharField(max_length=13, validators=[RegexValidator()], unique=True)
    category = models.ForeignKey("products.Category", on_delete=models.SET_NULL, related_name="user", null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=Role.choices, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.username:
            return self.username
        if self.username is None:
            return self.phone_number

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)
