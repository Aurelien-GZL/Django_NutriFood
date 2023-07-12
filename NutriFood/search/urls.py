from django.urls import path

from . import views

# Create namespace for the application
app_name = "search"

urlpatterns = [
    # Path: /search/
    path('', views.index, name='index'),
    # Path: /search/compare/
    # Referring to view "product_compare" in /search/views.py
    # Be careful to the order of the paths to avoid wrong referencing due to the more generic pattern
    # Here product_compare won't work if below product detail
    path('compare/', views.product_compare, name='product_compare'),
    # Path: /search/<product_id>/
    # Referring to view "product_detail" in /search/views.py
    path('<str:product_id>/', views.product_detail, name='product_detail'),

]