from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Creates initial info of the database (Users)"

    def handle(self, *args, **kwargs):
        # Admin
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@admin.com",
                password="admin"
            )
            self.stdout.write(self.style.SUCCESS("✔ Admin created"))
        else:
            self.stdout.write("⚠ Admin already exists")

        # Sissa
        if not User.objects.filter(username="sissa").exists():
            User.objects.create_user(
                username="sissa",
                email="sissa@goodbite.com",
                first_name="Cecília Maria",
                last_name="Rodrigues",
                password="sissa123"
            )
            self.stdout.write(self.style.SUCCESS("✔ Sissa user created"))
        else:
            self.stdout.write("⚠ Sissa user already exists")

        # Uri
        if not User.objects.filter(username="uri").exists():
            User.objects.create_user(
                username="uri",
                first_name="Oriol",
                last_name="Ramos Puig",
                email="uri@goodbite.com",
                password="uri123"
            )
            self.stdout.write(self.style.SUCCESS("✔ Uri user created"))
        else:
            self.stdout.write("⚠ Uri user already exists")

        # Anna
        if not User.objects.filter(username="anna").exists():
            User.objects.create_user(
                username="anna",
                first_name="Anna",
                last_name="Melkumyan",
                email="anna@goodbite.com",
                password="anna123"
            )
            self.stdout.write(self.style.SUCCESS("✔ Anna user created"))
        else:
            self.stdout.write("⚠ Anna user already exists")

        # Johanna
        if not User.objects.filter(username="johanna").exists():
            User.objects.create_user(
                username="johanna",
                first_name="Johanna",
                last_name="Nuñez",
                email="johanna@goodbite.com",
                password="johanna123"
            )
            self.stdout.write(self.style.SUCCESS("✔ Johanna user created"))
        else:
            self.stdout.write("⚠ Johanna user already exists")

        # Irene
        if not User.objects.filter(username="irene").exists():
            User.objects.create_user(
                username="irene",
                first_name="Irene",
                last_name="Cerván",
                email="irene@goodbite.com",
                password="irene123"
            )
            self.stdout.write(self.style.SUCCESS("✔ Irene user created"))
        else:
            self.stdout.write("⚠ Irene user already exists")

        self.stdout.write(self.style.SUCCESS("Users created !!!!"))
