import textwrap

from decouple import config
import requests
from bs4 import BeautifulSoup


class ContentParser:
    """Класс для парсинга, принимает аргументы: url: доменный адрес сайта,
    width: ширина строки в символах, save_images: сохранять ссылки на изображения."""

    UNNECESSARY_TAG_SELECTORS = [
        '[class*="footer"]',
        '[class*="header"]',
        '[class~="sidebar"]',
        '[class~="navigation"]',
        '[class*="page__top"]',
        '[class*="meta"]',
        '[class*="panel"]',
        '[class*="icons"]',
    ]

    def __init__(self, url: str, width: int = 0, save_images: bool = False):
        self.url = url
        self.width = width
        self.save_images = save_images

        self.user_agent = config('USER_AGENT')
        self.headers = {'accept': '*/*', 'user-agent': self.user_agent}

        try:
            response = requests.get(self.url, headers=self.headers)
            html = response.text
        except requests.exceptions.RequestException:
            html = f'Произошла ошибка подключения по адресу {self.url}'

        self.soup = BeautifulSoup(html, 'lxml')
        self.html_body = self.soup.body
        self.cleaned_data = ''

    def _exclude_unnecessary_tags(self):
        """Исключает не нужные данные из объекта soup."""
        for selector in self.UNNECESSARY_TAG_SELECTORS:
            tags = self.html_body.select(selector)
            for tag in tags:
                tag.decompose()

    def _get_content(self):
        """Очищает объект soup от всех тегов."""
        self.cleaned_data += 'Текст:\n' + self.html_body.get_text(' ', strip=True)

    def _make_line_width(self):
        """Определяет ширину строки в тексте."""
        self.cleaned_data = textwrap.fill(self.cleaned_data, self.width,
                                          replace_whitespace=False)

    def _add_cleaned_images(self):
        """Добавляет в текст ссылки на изображения."""
        self.cleaned_data += '\n\nИзображения:\n'
        images = self.html_body.find_all('img')
        for image in images:
            try:
                self.cleaned_data += image['src'] + '\n'
            except KeyError:
                pass

    def parse(self):
        """Основная функция, формирует cleaned_data."""
        self._exclude_unnecessary_tags()
        self._get_content()
        if self.width > 0:
            self._make_line_width()
        if self.save_images:
            self._add_cleaned_images()
        return self.cleaned_data
