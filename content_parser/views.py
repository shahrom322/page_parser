from django.http import HttpResponse
from django.shortcuts import render, redirect

from .content_parser import ContentParser


def main_page(request):
    """Выводит страницу с формой для заполнения данных для парсера и перенаправляет
    их на эндпоинт parse/."""

    return render(request, 'index.html')


def parse(request):
    """Принимает get запрос с параметрами. Возвращает файл в формате
    txt с спарсенными данными."""

    url = request.GET.get('url')
    width = int(request.GET.get('width', 0))
    save_images = True if request.GET.get('save_images') == 'on' else False

    content = ContentParser(url, width, save_images).parse()
    return HttpResponse(content, content_type='text/plain; charset=utf-8')
