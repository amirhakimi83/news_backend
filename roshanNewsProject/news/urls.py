from django.urls import path
from .views import *

urlpatterns = [
    path("news/", all_news, name="all_news"),
    path("news/insert/", insert_news, name="insert_news"),
    path('news/delete/', delete_news, name='delete_news')
]