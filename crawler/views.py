from django.http import HttpResponse
from django.shortcuts import render
from .models import Article

def index(request):
    return HttpResponse("Hello from your Django app!")

def articles_list(request):
    articles = Article.objects.all().only('title', 'url')[:100]
    return render(request, 'articles_list.html', {'articles': articles})
