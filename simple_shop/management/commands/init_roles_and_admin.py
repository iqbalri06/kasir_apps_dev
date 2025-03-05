from django.core.management.base import BaseCommand
from django.db import transaction
from simple_shop.models import Role, User

class Command(BaseCommand):
    help = 'Initialize default roles and create admin user'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create roles
            admin_role, _ = Role.objects.get_or_create(name='Admin')
            cashier_role, _ = Role.objects.get_or_create(name='Cashier')
            
            # Create admin user if it doesn't exist
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
            else:
                self.stdout.write(self.style.WARNING('Admin user already exists'))

            self.stdout.write(self.style.SUCCESS('Roles created successfully'))
