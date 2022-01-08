from django.urls import path

from .views import main_page, parse


urlpatterns = [
    path('', main_page, name='main'),
    path('parse/', parse, name='parse'),
]
