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
                content__icontains=query
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
