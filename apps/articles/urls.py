from django.urls import path
from apps.articles.views import *

app_name = 'articles'

urlpatterns = [
    path('', main, name='main'),
]