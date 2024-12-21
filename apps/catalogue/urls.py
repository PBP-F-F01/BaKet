from django.urls import path
from apps.catalogue.views import *

app_name = 'catalogue'

urlpatterns = [
    path('', catalogue_view, name='catalogue'),
    path('add-product/', create_product, name='add_product'),
    path('add-product-api/', add_product_api, name='add_product_api'), 
    path('product/<uuid:product_id>/', product_detail, name='product_detail'),
    path('add-review-ajax/', add_review_ajax, name='add_review_ajax'),
    path('json/', show_json, name='show_json'),
    path('prod-json/', product_list, name='prod_json'), 
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<uuid:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order/<int:order_id>/confirmation/', order_confirmation, name='order_confirmation'),
    path('like-review/', like_review, name='like_review'),
    path('review-json/<uuid:product_id>/', show_review_json, name='show_review_json'),
    path('create-review/', create_review_flutter, name='create_review_flutter'),
    path('calculate-ratings/', calculate_ratings, name='calculate_ratings'),
    path('has-reviewed/', has_reviewed, name='has_reviewed'),
    path('delete/<int:review_id>/', delete_review, name='delete_review'),
    path('cart-api/', view_cart_api, name='view_cart_api'),
    path('cart-count/', cart_count_api, name='cart_count_api'),
    path('checkout-api/', checkout_api, name='checkout_api'),
    path('api/csrf-token/', csrf_token_view, name='csrf_token'),
]
