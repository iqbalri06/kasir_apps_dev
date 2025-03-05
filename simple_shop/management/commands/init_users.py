from django.core.management.base import BaseCommand
from django.db import transaction
from simple_shop.models import Role, User

class Command(BaseCommand):
    help = 'Initialize default roles and users (admin and cashier)'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create roles
            admin_role, _ = Role.objects.get_or_create(name='Admin')
            cashier_role, _ = Role.objects.get_or_create(name='Cashier')
            
            # Create admin user
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123',
                    role=admin_role,
                    first_name='Admin',
                    last_name='User'
                )
                self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
            
            # Create cashier user
            if not User.objects.filter(username='cashier').exists():
                User.objects.create_user(
                    username='cashier',
                    email='cashier@example.com',
                    password='cashier123',
                    role=cashier_role,
                    first_name='Cashier',
                    last_name='User',
                    is_staff=True
                )
                self.stdout.write(self.style.SUCCESS('Cashier user created successfully'))

            self.stdout.write(self.style.SUCCESS('Default users created successfully'))
