from django.urls import path
from apps.catalogue.views import *

urlpatterns = [
    path('', catalogue_view, name='catalogue'),
    path('add-product/', create_product, name='add_product'),
    path('product/<uuid:product_id>/', product_detail, name='product_detail'),
    path('add-review-ajax/', add_review_ajax, name='add_review_ajax'),
     path('json/', show_json, name='show_json'),
]