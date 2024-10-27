from django.urls import path
from apps.user.views import *

urlpatterns = [
    path('settings', settings_view, name='settings_view'),
    path('upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
    path('update_name/', update_name, name='update_name'),
    path('update_birth_date/', update_birth_date, name='update_birth_date'),
    path('update_email/', update_email, name='update_email'),
    path('update_phone/', update_phone, name='update_phone'),
    path('update_gender/', update_gender, name='update_gender'),
]