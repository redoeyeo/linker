import scrapy
from scrapy.http import Response

from crawler.models import Author
from crawler.src.items import ArticleItem


class BearSpider(scrapy.Spider):
    name = "bear"
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'DOWNLOAD_DELAY': 1,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        },
    }

    def start_requests(self):
        yield scrapy.Request('https://bearblog.dev/discover/', cookies={
            'lang': 'ru'
        }, callback=self.parse)

    def parse(self, response: Response):
        print(f'Bear page: {response.url}')
        posts = response.xpath('//div/a[@href]/@href').getall()
        for post in posts:
            post = post.replace('//', '')
            post_link = f'https://{post}'
            yield response.follow(post_link, self.parse_blog)
        page = response.xpath(
            "//a[contains(@href,'page=') and contains(text(), 'Next')]/@href").get()
        if page:
            next_page = f'https://bearblog.dev/discover/{page}'
            yield response.follow(next_page, self.parse)

    async def parse_blog(self, response):
        aurl = f'https://{response.url.split('/')[2]}'
        author, created = await Author.objects.aget_or_create(url=aurl)

        title = response.xpath('//main/h1/text()').get()
        content = []
        lines = response.xpath(
            '//main//text()[not(ancestor::script)]').getall()
        content = [el for el in lines if len(el.strip()) > 0]
        content = '\n'.join(content)
        yield ArticleItem(
            title=title,
            author_id=author.id,
            url=response.url,
            content=content
        )
