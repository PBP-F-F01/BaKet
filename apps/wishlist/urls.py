from django.urls import path
from apps.wishlist.views import *

urlpatterns = [
    path('', wishlist_view, name='wishlist'),
    path('add/<uuid:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<uuid:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('toggle/<uuid:product_id>/', toggle_wishlist, name='toggle_wishlist'),
    path('is_in_wishlist/<uuid:product_id>/', is_in_wishlist, name='is_in_wishlist'),
    path('toggle-api/', toggle_wishlist_api, name='toggle_wishlist_api'),
    path('json/', show_json, name='show_json'),
]