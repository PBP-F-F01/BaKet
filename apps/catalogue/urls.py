from django.urls import path
from apps.catalogue.views import *

urlpatterns = [
    path('', catalogue_view, name='catalogue'),
    path('add-product/', create_product, name='add_product'),
    path('product/<uuid:product_id>/', product_detail, name='product_detail'),
    path('review/', review_rate, name='review'),
]