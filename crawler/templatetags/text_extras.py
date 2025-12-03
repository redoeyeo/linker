import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight(text, query):
    """
    Выделяет все вхождения query в text с помощью HTML-тега mark
    """
    if not query or not text:
        return text

    # Экранируем специальные символы в запросе для безопасного использования в регулярном выражении
    escaped_query = re.escape(query.strip())

    # Создаем регулярное выражение для поиска с учетом регистра
    pattern = f'({escaped_query})'

    # Заменяем найденные вхождения на тег mark с классом bg-danger
    highlighted = re.sub(
        pattern, r'<mark class="bg-danger text-white">\1</mark>', text, flags=re.IGNORECASE)

    # Помечаем результат как безопасный HTML
    return mark_safe(highlighted)
