from django.contrib import admin

# Register your models here.
from .models import Product, Profile

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_by')
    search_fields = ('name',)
    list_filter = ('created_by',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "birthdate")
    search_fields = ("user__username", "user__email", "phone_number")