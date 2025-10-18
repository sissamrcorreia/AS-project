from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from GoodBite.models import Product
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = "Clears all seeded users and products from the database"

    def handle(self, *args, **kwargs):
        # Delete all products
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✔ All products deleted"))

        # Delete specific seeded users (excluding admin if needed)
        seeded_usernames = [
            "sissaCustomer", "sissaSeller",
            "uriCustomer", "uriSeller",
            "annaCustomer", "annaSeller",
            "johannaCustomer", "johannaSeller",
            "ireneCustomer", "ireneSeller"
        ]
        users = User.objects.filter(username__in=seeded_usernames)
        users.delete()
        self.stdout.write(self.style.SUCCESS("✔ Seeded users deleted"))

        # Optionally delete the Customer and Seller groups if they were created by the seed
        Group.objects.filter(name__in=["Customer", "Seller"]).delete()
        self.stdout.write(self.style.SUCCESS("✔ Customer and Seller groups deleted"))

        self.stdout.write(self.style.SUCCESS("🎉 Database cleared successfully!"))