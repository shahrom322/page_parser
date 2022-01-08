from django.test import TestCase
from django.urls import reverse

from .content_parser import ContentParser

# Ожидаемый результат для теста парсера
EXPECTED_RESULT = '''\
Текст:
http://info.cern.ch http://info.cern.ch - home of the first
website From here you can: Browse the first website Browse the first
website using the line-mode browser simulator Learn about the birth of
the web Learn about CERN, the physics laboratory where the web was
born
Изображения:
'''


class ViewsTest(TestCase):
    """Тестирование контроллеров сайта."""

    def test_main_view_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_main_view_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

    def test_parser_view_status(self):
        response = self.client.get(reverse('parse'))
        self.assertEqual(response.status_code, 200)

    def test_parser_view_correct_content_type(self):
        response = self.client.get(reverse('parse'))
        self.assertEqual(response['content-type'], 'text/plain; charset=utf-8')

    def test_parser_correct_data(self):
        self.maxDiff = None

        url = 'http://info.cern.ch/'
        width = 70
        save_images = True
        content = ContentParser(url, width, save_images).parse()
        self.assertEqual(content, EXPECTED_RESULT)

    def test_parser_incorrect_url(self):
        url = 'test.url'
        content = ContentParser(url).parse()
        expected_result = '''Текст:\nПроизошла ошибка подключения по адресу test.url'''
        self.assertEqual(content, expected_result)
