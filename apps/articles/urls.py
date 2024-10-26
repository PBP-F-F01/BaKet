from django.urls import path
from apps.articles.views import *

app_name = 'articles'

urlpatterns = [
    path('', main, name='main'),
    path('dummy/', dummy_article, name='dummy_article'),
    path('dummymain/', dummy_main, name='dummy_main'),
    path('main/', show_main, name="show_main"),
]