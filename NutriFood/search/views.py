from django.shortcuts import render
from .models import Product
from django.http import HttpResponse

# Create your views here.

def index(request):
    product_all = Product.objects.all()
    context = {"product_all": product_all}
    return render(request, "search/index.html", context)


# Product_id is extracted from the URL matching the "product_detail" pattern in search/urls.py
def product_detail(request, product_id):
    # Access "Product" object database and get records from the URL product_id
    product = Product.objects.get(id=product_id)
    # Dictionary holding data to pass to the template, here product records for the given product_id
    context = {"product": product}
    # Render function takes the request, the template path, and the context dictionary as arguments
    # This function combines the template with the provided context data and generates an HTML response, which is sent back to the client.
    return render(request, "search/product_detail.html", context)


def product_compare(request):
    distinct_categories = Product.objects.values('category')\
        .distinct()\
        .order_by('category')
    if request.method == 'POST':
        selected_category = request.POST.get('category')
        selected_product = request.POST.get('product_name')
        related_products = Product.objects.filter(category=selected_category)\
            .order_by('product_name')
        alternative_products = Product.objects.filter(category=selected_category)\
            .order_by('nutriscore_score')[:5]
        try:
            product_info = Product.objects.get(product_name=selected_product)
        except Product.DoesNotExist:
            product_info = None
        context = {
            "product_info": product_info,
            "related_products": related_products,
            "distinct_categories": distinct_categories,
            "selected_category": selected_category,
            "alternative_products": alternative_products,
            "selected_product": selected_product
        }
        return render(request, "search/product_compare.html", context)
    else:
        selected_category = request.GET.get('category')  # Get the selected category from the query parameters
        related_products = Product.objects.filter(category=selected_category) \
            .order_by('product_name')
        context = {
            "related_products": related_products,
            "distinct_categories": distinct_categories,
            "selected_category": selected_category,
    }
        return render(request, "search/product_compare.html", context)
