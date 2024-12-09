from django.urls import path
from apps.authentication.views import login, register

app_name = 'apps.authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),

]