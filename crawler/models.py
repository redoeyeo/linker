from django.db import models



class Author(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    article_authors = models.ManyToManyField(
        'Article', related_name='article_authors', blank=True)
    video_authors = models.ManyToManyField(
        'Video', related_name='video_authors', blank=True)
    book_authors = models.ManyToManyField(
        'Book', related_name='book_authors', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or f"Author {self.id}"

    class Meta:
        db_table = 'authors'


class Article(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    author = models.ForeignKey(
        'Author', on_delete=models.CASCADE, related_name='authored_articles')

    def __str__(self):
        return self.title or f"Article {self.id}"

    class Meta:
        db_table = 'articles'


class Video(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    publication_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        'Author', on_delete=models.CASCADE, related_name='authored_videos')

    def __str__(self):
        return self.title or f"Video {self.id}"

    class Meta:
        db_table = 'videos'


class Book(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey(
        'Author', on_delete=models.CASCADE, related_name='authored_books')

    def __str__(self):
        return self.title or f"Book {self.id}"

    class Meta:
        db_table = 'books'


class WebPageArchive(models.Model):
    url = models.URLField()
    html = models.TextField()
    archived = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

    class Meta:
        db_table = 'web_page_archives'
