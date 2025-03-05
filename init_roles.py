import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')
django.setup()

from simple_shop.models import Role

# Default roles
default_roles = [
    "Admin",
    "Cashier"
]

def create_default_roles():
    for role_name in default_roles:
        Role.objects.get_or_create(name=role_name)
        print(f"Role '{role_name}' created or already exists")

if __name__ == "__main__":
    print("Creating default roles...")
    create_default_roles()
    print("Done!")
