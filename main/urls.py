from django.urls import path
from .views import index
from .views import register, login_user

app_name = 'main'

urlpatterns = [
    path('', index),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    # path('logout/', logout_user, name='logout'),
]