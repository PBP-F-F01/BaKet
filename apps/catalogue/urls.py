from django.urls import path
from apps.catalogue.views import *

app_name = 'catalogue'

urlpatterns = [
    path('', catalogue_view, name='catalogue'),
    path('add-product/', create_product, name='add_product'),
    path('product/<uuid:product_id>/', product_detail, name='product_detail'),
    path('add-review-ajax/', add_review_ajax, name='add_review_ajax'),
    path('json/', show_json, name='show_json'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<uuid:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order/<int:order_id>/confirmation/', order_confirmation, name='order_confirmation'),
]