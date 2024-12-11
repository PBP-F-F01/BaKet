from django.urls import path
from apps.authentication.views import login, register, logout

app_name = 'apps.authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
]