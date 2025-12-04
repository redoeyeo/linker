
from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)
    article_authors: models.ManyToManyField = models.ManyToManyField(
        'Article', related_name='article_authors', blank=True)
    video_authors: models.ManyToManyField = models.ManyToManyField(
        'Video', related_name='video_authors', blank=True)
    book_authors: models.ManyToManyField = models.ManyToManyField(
        'Book', related_name='book_authors', blank=True)

    class Meta:
        db_table = 'authors'


class Article(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    author = models.ForeignKey(
        'Author', on_delete=models.CASCADE, related_name='authored_articles')

    @property
    def lines(self):
        if not self.content:
            return []
        content = str(self.content)
        lines = content.splitlines()
        if len(lines) == 1:
            lines = content.split('.')
            lines = [f'{line}.'.strip() for line in lines]
        return lines

    class Meta:
        db_table = 'articles'


class Video(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    publication_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        'Author', on_delete=models.CASCADE, related_name='authored_videos')

    class Meta:
        db_table = 'videos'


class Book(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey(
        'Author', on_delete=models.CASCADE, related_name='authored_books')

    class Meta:
        db_table = 'books'


class WebPageArchive(models.Model):
    url = models.URLField()
    html = models.TextField()
    archived = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'web_page_archives'
