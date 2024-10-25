from django.urls import path
from apps.wishlist.views import *

urlpatterns = [
    path('', wishlist_view, name='wishlist'),
    path('add/<uuid:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<uuid:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]