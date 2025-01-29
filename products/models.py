from django.db import models
from django.utils.text import slugify
from .managers import CategoryManager
from django.utils.translation import gettext as _


class Category(models.Model):
    parent = models.ForeignKey('self', related_name="children", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="category_icons/", null=True, blank=True)

    objects = CategoryManager()

    def __str__(self):
        return self.name

    def ads_count(self):
        ads_count = self.products.count()
        for child in self.children.all():
            ads_count += child.ads_count()
        return ads_count


class Product(models.Model):
    class Currency(models.TextChoices):
        uzs = "uzs", _("UZS")
        rub = "rub", _("RUB")
        usd = "usd", _("USD")

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        PENDING = 'pending', 'Pending'

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    phone_number = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    author = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    validate_address = models.ForeignKey('common.Address', on_delete=models.SET_NULL, related_name='products',
                                         null=True)
    currency = models.CharField(max_length=3, choices=Currency.choices, default=Currency.uzs)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    is_mine = models.BooleanField(default=False, null=True)
    status = models.CharField(max_length=50, default=Status.PENDING, choices=Status.choices, null=True)
    expires_at = models.DateTimeField(null=True)
    seller = models.ForeignKey("accounts.User", related_name="products", on_delete=models.CASCADE, blank=True,
                               null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Image(models.Model):
    image = models.ImageField(upload_to='product_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class PopularSearchWord(models.Model):
    word = models.CharField(max_length=255, unique=True)
    count = models.IntegerField()

    def __str__(self):
        return self.word
