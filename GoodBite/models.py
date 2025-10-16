from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    class Meta:
        permissions = [
            ("can_create_product", "Can create products"),
            ("can_edit_own_product", "Can edit own products"),
            ("can_view_product", "Can view products"),
        ]

    def __str__(self):
        return self.name