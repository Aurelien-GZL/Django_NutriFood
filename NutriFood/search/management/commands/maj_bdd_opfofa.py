from django.core.management.base import BaseCommand
import requests
from search.models import Product

# Command: python manage.py maj_bdd_opfofa Mueslis Chocolat Biscuits Pains Sauces


class Command(BaseCommand):
    help = 'Fetches data from the API and imports it into the database'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('categories', nargs='*', type=str)
        parser.add_argument('--limit', type=int, default=100)

    def handle(self, *args, **kwargs):
        # Truncate the Product table
        Product.objects.all().delete()

        fields = ['product_name', 'nutriscore_score', 'id', 'brands',
                  'nutriscore_grade']

        categories = kwargs['categories']

        url = "https://fr.openfoodfacts.org/cgi/search.pl"

        for category in categories:

            params = {
                "action": "process",
                "tagtype_0": "categories",
                "tag_contains_0": "contains",
                "tag_0": category,
                "page_size": kwargs['limit'],
                "fields": ",".join(fields),
                "json": "true",
            }
            response = requests.get(url, params=params)

            if response.status_code == 200:
                products_data = response.json()
                products_full = products_data['products']

                # Add field names for each product even if empty
                # Use of dictionary comprehension nested in list comprehension
                # Merging of 2 dict to include category with syntax **
                # Get method to obtain dict key value (field)
                # Check that all fields have a value otherwise product is excluded
                products_full = [
                    {
                        **{field: product.get(field) for field in fields},
                        'category': category
                    }
                    for product in products_full
                    if all(product.get(field) for field in fields)
                ]

            else:
                print(f"Failed to retrieve products for category '{category}'. Status code: {response.status_code}")

            product_instances = []
            for product in products_full:
                # Create a new Product instance
                product_instances.append(
                    Product(
                        id=product['id'],
                        category=product['category'],
                        brand=product['brands'],
                        nutriscore_grade=product['nutriscore_grade'],
                        nutriscore_score=product['nutriscore_score'],
                        product_name=product['product_name']
                    )
                )

            # Save all products to the database in one step
            Product.objects.bulk_create(product_instances)

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {len(product_instances)} products"))
