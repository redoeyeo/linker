from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from .models import Article, Author, engine

Session = sessionmaker(bind=engine)


class ArticlesPipeline:
    def open_spider(self, spider):
        """Вызывается при запуске паука. Создает новую сессию."""
        self.session = Session()

    def close_spider(self, spider):
        """Вызывается при завершении паука. Закрывает сессию."""
        self.session.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter.get('author_id'):
            raise DropItem('All articles should contain author_id url')
        author_id = adapter.get('author_id')
        try:
            author = self.session.query(Author).filter(
                Author.id == author_id).one()
        except NoResultFound:
            raise DropItem('Не удалось найти автора')

        # Проверяем, существует ли уже статья с таким URL
        existing_article = self.session.query(Article).filter(
            Article.url == adapter['url']).first()
        if existing_article:
            raise DropItem('Уже сохранена статья с данным url')

        article = Article(
            title=adapter['title'],
            content=adapter['content'],
            url=adapter['url'],
            author=author
        )
        self.session.add(article)
        self.session.commit()
        return item
