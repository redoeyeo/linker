import logging

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from crawler.models import Article, Author

logger = logging.getLogger(__name__)


class ArticlesPipeline:
    def open_spider(self, spider):
        """Вызывается при запуске паука."""
        pass

    def close_spider(self, spider):
        """Вызывается при завершении паука."""
        pass

    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter.get('author_id'):
            raise DropItem('All articles should contain author_id')

        try:
            author = await Author.objects.aget(id=adapter['author_id'])
        except Author.DoesNotExist:
            raise DropItem('Не удалось найти автора')

        # Проверяем, существует ли уже статья с таким URL
        if await Article.objects.filter(url=adapter['url']).aexists():
            raise DropItem('Уже сохранена статья с данным url')

        # Создаем и сохраняем статью в транзакции
        article = Article(
            title=adapter['title'],
            content=adapter['content'],
            url=adapter['url'],
            author=author
        )
        await article.asave()
        return item
