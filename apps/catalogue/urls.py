from django.urls import path
from apps.catalogue.views import *

urlpatterns = [
    path('', catalogue_view, name='catalogue'),
    path('add-product/', create_product, name='add_product'),
    path('product/<uuid:product_id>/', product_detail, name='product_detail'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order/<int:order_id>/confirmation/', order_confirmation, name='order_confirmation'),
]