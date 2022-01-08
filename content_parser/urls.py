from django.urls import path

from .views import content_parser


urlpatterns = [
    path('', content_parser),
]