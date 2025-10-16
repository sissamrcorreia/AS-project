from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create user roles and assign permissions'

    def handle(self, *args, **kwargs):
        # Create roles
        customer_group, created = Group.objects.get_or_create(name='Customer')
        seller_group, created = Group.objects.get_or_create(name='Seller')

        # Get permissions
        create_product_perm = Permission.objects.get(codename='can_create_product')
        edit_own_product_perm = Permission.objects.get(codename='can_edit_own_product')
        view_product_perm = Permission.objects.get(codename='can_view_product')

        # Assign to groups
        seller_group.permissions.add(create_product_perm, edit_own_product_perm)
        customer_group.permissions.add(view_product_perm)  # View-only for customers

        self.stdout.write(self.style.SUCCESS('Roles and permissions set up!'))