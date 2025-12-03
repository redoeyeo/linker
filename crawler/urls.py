from django.urls import path

from . import views

urlpatterns = [
    path('articles', views.search_articles, name='search_articles'),
    path('love', views.love_message, name='love_message'),
]
