import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')
django.setup()

from simple_shop.models import Product

# Delete all products
Product.objects.all().delete()
