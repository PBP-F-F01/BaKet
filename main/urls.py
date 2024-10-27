from django.urls import path
from .views import index
from .views import register, login_user, logout_user, get_cart_count
from django.conf import settings
from django.conf.urls.static import static


app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('cart/count/', get_cart_count, name='get_cart_count'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)