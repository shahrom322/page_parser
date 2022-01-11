from django.core.management import BaseCommand

from content_parser.content_parser import ContentParser


class Command(BaseCommand):
    help = 'Парсит данные с сайта. python manage.py <url> <width> <save_images>'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL адрес сайта. https://example.com')
        parser.add_argument('width',  default=50, type=int, help='Ширина строки в символах')
        parser.add_argument('save_images', default=False, type=bool, help='Введите 1, что бы сохранять изображения')

    def handle(self, *args, **options):
        content = ContentParser(
            options.get('url'),
            options.get('width'),
            options.get('save_images')
        ).parse()
        self.stdout.write(content)
