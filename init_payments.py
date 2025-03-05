import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')
django.setup()

from simple_shop.models import Payment

# Default payment methods
default_payments = [
    ('cash', 'Tunai'),
    ('qris', 'QRIS'),
    ('debit', 'Debit')
]

def create_default_payments():
    for method_code, method_name in default_payments:
        Payment.objects.get_or_create(
            method=method_code
        )
        print(f"Payment method '{method_name}' created or already exists")

if __name__ == "__main__":
    print("Creating default payment methods...")
    create_default_payments()
    print("Done!")
