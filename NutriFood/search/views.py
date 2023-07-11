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
