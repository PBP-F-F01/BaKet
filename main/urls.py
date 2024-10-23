from django.urls import path
from main.views import index, show_product, create_product, product_detail

urlpatterns = [
    path('', index),
    path('products/', show_product, name='show_product'),
    path('create_product/', create_product, name='create_product'),
    path('product/<uuid:product_id>/', product_detail, name='product_detail'),
]