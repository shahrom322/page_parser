import textwrap

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class ContentParser:
    """Класс для парсинга, принимает аргументы: url: доменный адрес сайта,
    width: ширина строки в символах, save_images: сохранять ссылки на изображения."""

    def __init__(self, url: str, width: int = 0, save_images: bool = False):
        self.url = url
        self.width = width
        self.save_images = save_images

        # Имитируем реального User-Agent библиотекой fake_useragent
        self.user_agent = UserAgent()
        self.headers = {'accept': '*/*', 'user-agent': self.user_agent.chrome}

        try:
            response = requests.get(self.url, headers=self.headers)
            html = response.text
        except requests.exceptions.RequestException:
            html = f'Произошла ошибка подключения по адресу {self.url}'

        self.soup = BeautifulSoup(html, 'lxml')
        self.cleaned_data = ''

    def _clean_data(self):
        """Очищает объект soup от всех тегов."""
        self.cleaned_data += 'Текст:\n' + self.soup.get_text(' ', strip=True)

    def _make_line_width(self):
        """Определяет ширину строки в тексте."""
        self.cleaned_data = textwrap.fill(self.cleaned_data, self.width,
                                          replace_whitespace=False)

    def _add_cleaned_images(self):
        """Добавляет в текст ссылки на изображения."""
        self.cleaned_data += '\nИзображения:\n'
        images = self.soup.find_all('img')
        for image in images:
            try:
                self.cleaned_data += image['src'] + '\n'
            except KeyError:
                pass

    def parse(self):
        """Основная функция, формирует cleaned_data."""
        self._clean_data()
        if self.width > 0:
            self._make_line_width()
        if self.save_images:
            self._add_cleaned_images()
        return self.cleaned_data
