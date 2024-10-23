from django.urls import path
from apps.catalogue.views import *

urlpatterns = [
    path('', catalogue_view, name='catalogue'),
    path('add-product/', add_product, name='add_product'),
]