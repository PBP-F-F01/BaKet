from django.urls import path
from apps.feeds.views import *

app_name = 'feeds'

urlpatterns = [
    path('', show_all, name='show_all'),
    path('tabs/<str:all_tabs>/', change_tabs, name='change_tabs'),
    path('create/', create_post, name='create_post'),
    path('json/', json, name='json'),
    path('json/<str:id>/', json_by_id, name='json_by_id'),
]