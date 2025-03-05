import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')
django.setup()

from simple_shop.models import Category

# Default categories
default_categories = [
    "Makanan",
    "Minuman",
    "Snack",
    "Alat Tulis",
    "Elektronik",
    "Lainnya"
]

def create_default_categories():
    for category_name in default_categories:
        Category.objects.get_or_create(name=category_name)
        print(f"Category '{category_name}' created or already exists")

if __name__ == "__main__":
    print("Creating default categories...")
    create_default_categories()
    print("Done!")
