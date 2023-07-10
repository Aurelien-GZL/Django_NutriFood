import requests
import json
import pandas as pd
from search.models import Product

##########
# 1. test for one category
##########

def get_product_details():
    url = f"https://fr.openfoodfacts.org/cgi/search.pl"
    params = {
        "action": "process"
        , "tagtype_0": "categories"
        , "tag_contains_0": "contains"
        , "tag_0": "Pains"
        , "page_size": 3
        , "json": "true"
        , "fields": ",".join(fields_test)
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        product_data = response.json()
        return product_data
    else:
        print(f"Failed to retrieve product details. Status code: {response.status_code}")
        return None


fields_test = ['product_name', 'nutriscore_score', 'id', 'brands', 'nutriscore_grade']

product_details = get_product_details()

# Read JSON file with indent
product_details_json_view = json.dumps(product_details, indent=3)

# Transform to dataframe using normalize
df_product_detail = pd.json_normalize(
    product_details
    , record_path="products"
    # , meta=["_id"]
    , errors='ignore')

##########
# 2. Get product information for 5 categories, 100 products max per category
##########

# Function to make API request based on category and limiting to a number of products per category


def get_products_by_category(category, limit, api_fields):
    url = f"https://fr.openfoodfacts.org/cgi/search.pl"
    params = {
        "action": "process"
        , "tagtype_0": "categories"
        , "tag_contains_0": "contains"
        , "tag_0": category
        , "page_size": limit
        , "fields": ",".join(api_fields)
        , "json": "true"
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
            {**{field: product.get(field) for field in api_fields}, 'category': category}
            for product in products_full
            if all(product.get(field) for field in api_fields)
        ]

        return products_full

    else:
        print(f"Failed to retrieve products for category '{category}'. Status code: {response.status_code}")
        return []


# Define categories, fields
categories = ['Mueslis', 'Chocolat', 'Biscuits', 'Pains', 'Sauces' ]
products_per_category = 3
fields = ['product_name', 'nutriscore_score', 'id', 'brands', 'nutriscore_grade']

# Declare empty list and add product information for each category in the list
all_products = []
for category in categories:
    products = get_products_by_category(category, products_per_category, fields)
    all_products.extend(products)

# Read JSON file with indent
all_products_json_view = json.dumps(all_products, indent=3)
