from django.core.management.base import BaseCommand
from scrapy.cmdline import execute


class Command(BaseCommand):
    help = 'Run Scrapy commands from within Django'


    def add_arguments(self, parser):
        # Принимаем все аргументы как есть — передадим их напрямую в Scrapy
        parser.add_argument('scrapy_args', nargs='*', type=str)

    def handle(self, *args, **options):
        # Собираем аргументы для Scrapy
        scrapy_args = ['scrapy'] + options['scrapy_args']
        execute(scrapy_args)
