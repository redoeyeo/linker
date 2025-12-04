import random

from django.db.models import Q
from django.shortcuts import render

from .forms import SearchForm
from .models import Article


def search_articles(request):
    form = SearchForm(request.GET or None)
    articles = []
    search_query = ''

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            articles = Article.objects.filter(
                Q(content__icontains=query) | Q(title__icontains=query)

            ).order_by('title')
            search_query = query

    return render(request, 'articles_list.html', {
        'form': form,
        'articles': articles,
        'search_query': search_query
    })


def index(request):
    """
    Главная страница с навигацией по разделам приложения
    """
    return render(request, 'index.html')


def love_message(request):
    messages = [
        "Марина, ты самое прекрасное, что случилось со мной!",
        "Любовь моя Марина, каждый день с тобой — как праздник!",
        "Мариночка, твоя улыбка делает мой мир ярче!",
        "Для меня нет никого прекраснее, чем ты, Марина!",
        "Спасибо, что ты есть, моя любимая Марина!",
        "Ты — мое вдохновение, моя радость, моя Марина!",
        "Каждый момент с тобой я ценю, родная Марина!",
        "Марина, ты делаешь мою жизнь по-настоящему счастливой!",
        "Ты — самое дорогое сокровище в моей жизни, Марина!",
        "Без тебя мир был бы серым, спасибо, что ты есть, Марина!"
    ]
    return render(request, 'love.html', {'message': random.choice(messages)})
