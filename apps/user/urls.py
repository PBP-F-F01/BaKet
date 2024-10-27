from django.urls import path
from apps.user.views import *

urlpatterns = [
    path('settings', settings_view, name='wishlist'),
    path('upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
]