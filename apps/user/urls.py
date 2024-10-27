from django.urls import path
from apps.user.views import *

urlpatterns = [
    path('settings', settings_view, name='wishlist'),
]