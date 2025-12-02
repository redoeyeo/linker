
import pytest
from scrapy.http import Request, TextResponse

from crawler.models import Author
from crawler.src.items import ArticleItem
from crawler.src.spiders.bear import BearSpider
from crawler.src.spiders.zyg import PavelSpider


@pytest.mark.django_db
class TestBearSpider:
    @pytest.fixture
    def spider(self):
        return BearSpider()

    def test_parse_discover_page(self, spider: BearSpider):
        """Test parsing of bearblog discover page"""
        body = """
        <html>
            <div><a href="//blog1.bearblog.dev">Blog 1</a></div>
            <div><a href="//blog2.bearblog.dev">Blog 2</a></div>
            <a href="?page=2" class="next">Next</a>
        </html>
        """
        response = TextResponse(
            url='https://bearblog.dev/discover/',
            body=body,
            encoding='utf-8'
        )

        results = list(spider.parse(response))

        # Check that we have requests for individual blogs
        blog_requests = [r for r in results if isinstance(
            r, Request) and 'blog' in r.url]
        print(blog_requests)
        assert len(blog_requests) == 3
        assert 'blog1.bearblog.dev' in blog_requests[0].url
        assert 'blog2.bearblog.dev' in blog_requests[1].url
        assert blog_requests[2].url == 'https://bearblog.dev/discover/?page=2'
        # Check that we have request for next page
        next_page_requests = [r for r in results if 'page=2' in r.url]
        assert len(next_page_requests) == 1

    @pytest.mark.asyncio
    async def test_parse_blog_page(self, spider: BearSpider):
        """Test parsing of individual blog page"""
        body = """
        <html>
            <main>
                <h1>Test Article</h1>
                <p>First paragraph</p>
                <p>Second paragraph</p>
            </main>
        </html>
        """
        response = TextResponse(
            url='https://testblog.bearblog.dev/post',
            body=body,
            encoding='utf-8'
        )

        results = [r async for r in spider.parse_blog(response)]

        # Check that we yield an ArticleItem
        assert len(results) == 1
        assert isinstance(results[0], ArticleItem)
        assert results[0]['title'] == 'Test Article'
        assert 'First paragraph' in results[0]['content']
        assert 'Second paragraph' in results[0]['content']
        assert results[0]['author_id'] == 1
        assert results[0]['url'] == 'https://testblog.bearblog.dev/post'
        saved = await Author.objects.aget(id=1)
        assert saved.url == 'https://testblog.bearblog.dev'


class TestPavelSpider:
    @pytest.fixture
    def spider(self):
        return PavelSpider()

    def test_parse_main_page(self, spider):
        """Test parsing of main zygmantovich page"""
        body = """
        <html>
            <a href="/blog" class="read-more">ЧИТАТЬ</a>
        </html>
        """
        response = TextResponse(
            url='https://zygmantovich.com/',
            body=body,
            encoding='utf-8'
        )

        results = list(spider.parse(response))

        # Check that we have request for blog page
        assert len(results) == 1
        assert isinstance(results[0], Request)
        assert '/blog' in results[0].url

    def test_parse_blog_list(self, spider):
        """Test parsing of blog list page"""
        body = """
        <html>
            <article id="post-1">
                <a href="/article1" rel="bookmark">Article 1</a>
            </article>
            <article id="post-2">
                <a href="/article2" rel="bookmark">Article 2</a>
            </article>
            <nav id="nav-below">
                <a href="/page/2">Next</a>
            </nav>
        </html>
        """
        response = TextResponse(
            url='https://zygmantovich.com/blog',
            body=body,
            encoding='utf-8'
        )

        results = list(spider.parse_blog(response))

        # Check that we have requests for individual articles
        article_requests = [r for r in results if isinstance(
            r, Request) and '/article' in r.url]
        assert len(article_requests) == 2
        assert '/article1' in article_requests[0].url
        assert '/article2' in article_requests[1].url

        # Check that we have request for next page
        next_page_requests = [r for r in results if '/page/2' in r.url]
        assert len(next_page_requests) == 1

    def test_parse_article(self, spider):
        """Test parsing of individual article page"""
        body = """
        <html>
            <h1 class="entry-title"><span>Test Article Title</span></h1>
            <div class="e-content">
                <p>Article content paragraph 1</p>
                <p>Article content paragraph 2</p>
            </div>
        </html>
        """
        response = TextResponse(
            url='https://zygmantovich.com/article1',
            body=body,
            encoding='utf-8'
        )

        results = list(spider.parse_article(response))

        # Check that we yield an ArticleItem
        assert len(results) == 1
        assert isinstance(results[0], ArticleItem)
        assert results[0]['title'] == 'Test Article Title'
        assert 'Article content paragraph 1' in results[0]['content']
        assert 'Article content paragraph 2' in results[0]['content']
        assert results[0]['url'] == 'https://zygmantovich.com/article1'
        assert results[0]['author_id'] == 1
