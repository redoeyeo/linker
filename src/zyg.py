from pathlib import Path

import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import CloseSpider, DropItem
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from models import Article, Author, engine

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


class PavelSpider(scrapy.Spider):
    name = "zygmantovich"
    custom_settings = {
        'CONCURRENT_REQUESTS': 3,
        'DOWNLOAD_DELAY': 1,
        'DEFAULT_REQUEST_HEADERS':  {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        },
        'LOG_LEVEL': 'DEBUG',
        'ITEM_PIPELINES': {
            ArticlesPipeline: 300,
        },
    }

    def start_requests(self):
        """Инициализация паука и получение author_id перед началом работы."""
        session = Session()
        try:
            author = session.query(Author).filter(
                Author.first_name == 'Павел',
                Author.last_name == 'Зыгмантович'
            ).one()
            self.author_id = author.id
        except NoResultFound:
            self.logger.error("Author Павел Зыгмантович not found in database")
            raise CloseSpider(reason="Author not found in database")
        finally:
            session.close()

        yield scrapy.Request("https://zygmantovich.com/", self.parse)

    def parse(self, response):
        blog = response.xpath("//a[contains(text(),'ЧИТАТЬ')]/@href").get()
        yield response.follow(blog, self.parse_blog)

    def parse_blog(self, response):
        for article in response.xpath("//article[starts-with(@id, 'post-')]//a[@href and @rel='bookmark' and not(@title)]/@href").getall():
            yield response.follow(article, self.parse_article)
        next_page = response.xpath("//nav[@id='nav-below']//a/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse_blog)

    def handle_spider_error(self, failure, response, spider):
        """Обработка ошибок паука - остановка при любых исключениях"""
        self.logger.error(f"Spider error on {response.url}: {failure.value}")
        raise CloseSpider(reason=f"Error processing page: {failure.value}")

    def parse_article(self, response):
        article_url = response.url
        title = response.xpath("//h1[@class='entry-title']/span/text()").get()

        content = response.xpath("//div[@class='e-content']//text()").getall()
        content = ''.join([el.strip() for el in content])
        yield {
            'title': title,
            'content': content,
            'url': article_url,
            'author_id': self.author_id
        }
