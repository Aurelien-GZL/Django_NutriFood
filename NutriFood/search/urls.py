from django.urls import path

from . import views

urlpatterns = [
    # Path: /search/
    path('', views.index, name='index'),
    # Path: /search/<product_id>/
    # Referring to view "product" in /search/views.py
    path('<str:product_id>/', views.product_detail, name='product_detail'),
]