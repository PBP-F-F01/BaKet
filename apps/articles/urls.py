from django.urls import path
from apps.articles.views import *

app_name = 'articles'

urlpatterns = [
    path('', show_main, name="show_main"),
    path('artic/', artic_main, name='main'),
    path('dummy/', dummy_article, name='dummy_article'),
    path('dummymain/', dummy_main, name='dummy_main'),
    path('<uuid:id>/', show_article, name="show_article"),
    path('add_comment/<uuid:article_id>/', add_comment, name="add_comment"),
    path('update_comment/<str:comment_id>/', update_comment, name='update_comment'),
    path('delete_comment/<str:comment_id>/', delete_comment, name='delete_comment'),
    path("likeArticle/<str:article_id>/", like_article, name="like_article"),
    path("unlikeArticle/<str:article_id>/", unlike_article, name="unlike_article"),
    path("likeComment/<str:comment_id>/", like_comment, name="like_comment"),
    path("unlikeComment/<str:comment_id>/", unlike_comment, name="unlike_comment"),

    # JSON
    path('json/article/', json_article, name="json_article"),
    path('json/article/<str:id>/', json_by_id_aricle, name="json_by_id_aricle"),
    path('json/comment/', json_comment, name="json_comment"),
    path('json/comment/<str:article_id>/', json_comment_by_article, name="json_comment_by_article"),
    path('json/like/', json_like, name="json_like"),
    path('json/isLikeArticle/<str:article_id>/', is_like_article_view, name='is_like_article_view'),
    path('json/isLikeComment/<str:comment_id>/', is_like_comment_view, name='is_like_comment_view'),
    path('json/user/', current_user, name="current_user"),

    # JSON FOR FLUTTER
    path('json/flutter/main/', json_article_flutter, name="json_article_flutter"),
    path('json/flutter/article/<str:id>/', json_article_page_flutter, name="json_article_page_flutter"),
]