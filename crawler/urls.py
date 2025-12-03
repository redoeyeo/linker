from django.urls import path

from . import views

urlpatterns = [
    path('articles', views.search_articles, name='search_articles'),
]
