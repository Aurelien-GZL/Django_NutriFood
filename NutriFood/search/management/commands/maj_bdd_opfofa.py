from django.core.management.base import BaseCommand
import requests
from search.models import Product


class Command(BaseCommand):
    help = 'Fetches data from the API and imports it into the database'

    def handle(self, *args, **options):
        # Truncate the Product table
        Product.objects.all().delete()

        # Function to make API request based on category and limiting to a number of products per category
        def get_products_by_category(category, limit, api_fields):
            url = "https://fr.openfoodfacts.org/cgi/search.pl"
            params = {
                "action": "process",
                "tagtype_0": "categories",
                "tag_contains_0": "contains",
                "tag_0": category,
                "page_size": limit,
                "fields": ",".join(api_fields),
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
                        **{field: product.get(field) for field in api_fields},
                        'category': category
                    }
                    for product in products_full
                    if all(product.get(field) for field in api_fields)
                ]

                return products_full

            else:
                print(f"Failed to retrieve products for category '{category}'. Status code: {response.status_code}")
                return []

        # Define categories, fields
        categories = ['Mueslis', 'Chocolat', 'Biscuits', 'Pains', 'Sauces']
        products_per_category = 100
        fields = ['product_name', 'nutriscore_score', 'id', 'brands', 'nutriscore_grade']

        # Declare empty list and add product information for each category in the list
        all_products = []
        for category in categories:
            products = get_products_by_category(category, products_per_category, fields)
            all_products.extend(products)

        product_instances = []
        for product in all_products:
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
