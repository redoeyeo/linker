import scrapy
from scrapy.exceptions import CloseSpider

from ..items import ArticleItem


class PavelSpider(scrapy.Spider):
    name = "zygmantovich"
    custom_settings = {
        'CONCURRENT_REQUESTS': 3,
        'DOWNLOAD_DELAY': 1,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        },
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        """Инициализация паука и получение author_id перед началом работы."""
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
        yield ArticleItem(
            title=title,
            content=content,
            url=article_url,
            author_id=1
        )
