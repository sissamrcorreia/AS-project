from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .validators import ValidateImageFile
from phonenumber_field.modelfields import PhoneNumberField
import os
import uuid


def product_image_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('products', filename)

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True, validators=[ValidateImageFile()])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    stock = models.PositiveIntegerField(default=0)
    initial_stock = models.PositiveIntegerField(default=0)

    class Meta:
        permissions = [
            ("can_create_product", "Can create products"),
            ("can_edit_own_product", "Can edit own products"),
            ("can_view_product", "Can view products"),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:  # it does not exist yet
            self.initial_stock = self.stock
        super().save(*args, **kwargs)

    def sold_units(self):
        return max(0, self.initial_stock - self.stock)

    def total_revenue(self):
        return self.sold_units() * float(self.price)

def profile_image_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('profile', filename)

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    phone_number = PhoneNumberField(
        region="ES",           # ← Spain
        blank=True,            # allows empty
        null=True,             # needed for blank=True in most cases
        unique=True,
        max_length=20,
        help_text="Ejemplo: +34666123456"
    )
    
    birthdate = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to=profile_image_path, blank=True, null=True, validators=[ValidateImageFile()])

    def __str__(self):
        return f"Profile({self.user.username})"