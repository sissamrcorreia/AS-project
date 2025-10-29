from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from .validators import ValidateImageFile
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

    class Meta:
        permissions = [
            ("can_create_product", "Can create products"),
            ("can_edit_own_product", "Can edit own products"),
            ("can_view_product", "Can view products"),
        ]

    def __str__(self):
        return self.name

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
    phone_number = models.CharField(max_length=9, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to=profile_image_path, blank=True, null=True, validators=[ValidateImageFile()])

    def __str__(self):
        return f"Profile({self.user.username})"