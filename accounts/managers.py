from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def _create_user(self, username=None, phone_number=None, **extra_fields):
        if username is None:
            user = self.model(phone_number=phone_number, **extra_fields)
        else:
            user = self.model(username=username, **extra_fields)
        user.save(using=self._db)
        return user


    def create_user(self, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", self.model.Role.Seller)
        phone_number = extra_fields.pop("phone_number", None)
        if phone_number is None:
            raise ValueError("The phone must be")
        username = extra_fields.pop("username", None)
        return self._create_user(
            username=username, phone_number=phone_number, **extra_fields
        )



    def create_superuser(self, username, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("role", self.model.Role.Admin)

        if extra_fields.get("is_staff") is not True:
            raise ValidationError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValidationError("Superuser must have is_superuser=True.")

        return self._create_user(username, **extra_fields)

    def sellers(self):
        return self.filter(role=self.model.Role.SELLER)

    def admins(self):
        return self.filter(role=self.model.Role.ADMIN)