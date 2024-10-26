from django.urls import path
from apps.articles.views import *

app_name = 'articles'

urlpatterns = [
    path('', show_main, name="show_main"),
    path('artic/', artic_main, name='main'),
    path('dummy/', dummy_article, name='dummy_article'),
    path('dummymain/', dummy_main, name='dummy_main'),
    path('<uuid:id>/', show_article, name="show_article"),

    # JSON
    path('json/article/', json_article, name="json_article"),
    path('json/comment/', json_comment, name="json_comment"),
    path('json/comment/<uuid:id>/', json_comment_by_article, name="json_comment_by_article"),
    path('json/like/', json_like, name="json_like"),
]