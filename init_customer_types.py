import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_shop.settings')
django.setup()

from simple_shop.models import CustomerType

# Default customer types dengan discount rate dan points multiplier
default_types = {
    "Regular": {"discount_rate": 0, "points_multiplier": 1.0},
    "Silver": {"discount_rate": 5, "points_multiplier": 1.5},
    "Gold": {"discount_rate": 10, "points_multiplier": 2.0},
    "Platinum": {"discount_rate": 15, "points_multiplier": 2.5}
}

def create_default_customer_types():
    for type_name, values in default_types.items():
        CustomerType.objects.get_or_create(
            name=type_name,
            defaults={
                'discount_rate': values['discount_rate'],
                'points_multiplier': values['points_multiplier']
            }
        )
        print(f"CustomerType '{type_name}' created or already exists")

if __name__ == "__main__":
    print("Creating default customer types...")
    create_default_customer_types()
    print("Done!")
