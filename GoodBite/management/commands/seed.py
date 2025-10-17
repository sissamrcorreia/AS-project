from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files import File
from django.conf import settings
import os

from GoodBite.models import Product

User = get_user_model()

class Command(BaseCommand):
    help = "Creates initial users (Customers & Sellers) and demo products with images"

    def handle(self, *args, **kwargs):
        # === 1 Create roles ===
        customer_group, _ = Group.objects.get_or_create(name="Customer")
        seller_group, _ = Group.objects.get_or_create(name="Seller")

        users = [
            {"username": "admin", "first_name": "Admin", "last_name": "", "email": "admin@admin.com", "password": "admin", "is_superuser": True},
            {"username": "sissa", "first_name": "Cecília Maria", "last_name": "Rodrigues", "email": "sissa@goodbite.com", "password": "sissa123"},
            {"username": "uri", "first_name": "Oriol", "last_name": "Ramos Puig", "email": "uri@goodbite.com", "password": "uri123"},
            {"username": "anna", "first_name": "Anna", "last_name": "Melkumyan", "email": "anna@goodbite.com", "password": "anna123"},
            {"username": "johanna", "first_name": "Johanna", "last_name": "Nuñez", "email": "johanna@goodbite.com", "password": "johanna123"},
            {"username": "irene", "first_name": "Irene", "last_name": "Cerván", "email": "irene@goodbite.com", "password": "irene123"},
        ]

        for user_data in users:
            if user_data["username"] == "admin":
                if not User.objects.filter(username="admin").exists():
                    User.objects.create_superuser(**user_data)
                    self.stdout.write(self.style.SUCCESS("✔ Admin created"))
                else:
                    self.stdout.write("⚠ Admin already exists")
                continue

            base_username = user_data["username"]

            # Customer
            username_cust = f"{base_username}Customer"
            if not User.objects.filter(username=username_cust).exists():
                user_cust = User.objects.create_user(
                    username=username_cust,
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    email=f"{base_username.lower()}customer@goodbite.com",
                    password=user_data["password"]
                )
                user_cust.groups.add(customer_group)
                self.stdout.write(self.style.SUCCESS(f"✔ {username_cust} (Customer) created"))
            else:
                self.stdout.write(f"⚠ {username_cust} already exists")

            # Seller
            username_sell = f"{base_username}Seller"
            if not User.objects.filter(username=username_sell).exists():
                user_sell = User.objects.create_user(
                    username=username_sell,
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    email=f"{base_username.lower()}seller@goodbite.com",
                    password=user_data["password"]
                )
                user_sell.groups.add(seller_group)
                self.stdout.write(self.style.SUCCESS(f"✔ {username_sell} (Seller) created"))
            else:
                self.stdout.write(f"⚠ {username_sell} already exists")

        self.stdout.write(self.style.SUCCESS("🎉 All users created successfully!"))

        # === 2 Create demo products with images ===
        try:
            seller = User.objects.get(username="uriSeller")
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("⚠ 'uriSeller' not found. Products skipped."))
            return

        products = [
            {
                "name": "Jamón Ibérico",
                "description": "Jamón ibérico de bellota, curado artesanalmente con un sabor excepcional.",
                "price": 120.00,
                "image": "product1.jpg",
            },
            {
                "name": "Tortilla de Patatas",
                "description": "Clásica tortilla española jugosa, con huevos camperos y patatas de la huerta.",
                "price": 8.50,
                "image": "product2.jpg",
            },
            {
                "name": "Pan con Tomate",
                "description": "Rebanadas de pan crujiente con tomate rallado y aceite de oliva virgen extra.",
                "price": 4.00,
                "image": "product3.jpg",
            },
        ]

        # Folder where images are stored (relative to the project)
        images_folder = os.path.join(settings.BASE_DIR, "GoodBite", "static_seed_images")

        for pdata in products:
            image_path = os.path.join(images_folder, pdata["image"])
            if not os.path.exists(image_path):
                self.stdout.write(self.style.WARNING(f"⚠ Image not found: {image_path}"))
                continue

            with open(image_path, "rb") as f:
                product = Product.objects.create(
                    name=pdata["name"],
                    description=pdata["description"],
                    price=pdata["price"],
                    created_by=seller,
                )
                product.image.save(pdata["image"], File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f"✔ Created product: {pdata['name']}"))

        self.stdout.write(self.style.SUCCESS("🍽️ Demo products created successfully!"))