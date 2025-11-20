from django.urls import path
from . import views

urlpatterns = [
    path('crawler', views.index, name='index'),
    path('articles', views.articles_list, name='articles_list'),
]
