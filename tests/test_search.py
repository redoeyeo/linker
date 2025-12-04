import pytest

from crawler.models import Article, Author

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def articles():
    first_author = Author.objects.create(
        first_name='Павел',
        last_name='Краснов'
    )
    second_author = Author.objects.create(
        url='https://author-link.com'
    )
    Article.objects.create(title='Заметка о программировании',
                           content='Первый параграф\nВторой параграф',
                           url='https://someurl.com',
                           author=first_author)
    Article.objects.create(title='Заметка о психологии',
                           content='Сплошной текст. Без новой линии',
                           url='https://second.com',
                           author=second_author)


def test_empty_result(client):
    response = client.get(
        '/crawler/articles?query=Неизвестный вариант')
    context = response.context
    assert len(context['articles']) == 0


def test_by_articles_title(client):
    response = client.get(
        '/crawler/articles?query=заметка')
    context = response.context
    assert len(context['articles']) == 2


def test_by_content(client):
    response = client.get(
        '/crawler/articles?query=ТЕКСТ')
    context = response.context
    assert len(context['articles']) == 1
    article = context['articles'][0]
    assert article.lines == [
        'Сплошной текст.',
        'Без новой линии.'
    ]


def test_newline_output(client):
    response = client.get(
        '/crawler/articles?query=Заметка о программировании')
    context = response.context
    assert len(context['articles']) == 1
    article = context['articles'][0]
    assert article.lines == [
        'Первый параграф',
        'Второй параграф'
    ]
