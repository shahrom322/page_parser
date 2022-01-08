from django.shortcuts import render


def content_parser(request):
    return render(request, 'index.html')
