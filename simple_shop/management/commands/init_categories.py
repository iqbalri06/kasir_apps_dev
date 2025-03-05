from django.core.management.base import BaseCommand
from simple_shop.models import Category

class Command(BaseCommand):
    help = 'Initialize default product categories'

    def handle(self, *args, **options):
        categories = [
            'Cemilan',
            'Minuman',
            'Sembako',
            'Perabotan',
            'Lainnya',
        ]

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
            self.stdout.write(self.style.SUCCESS(f'Category "{category_name}" created'))

        self.stdout.write(self.style.SUCCESS('All categories created successfully'))
