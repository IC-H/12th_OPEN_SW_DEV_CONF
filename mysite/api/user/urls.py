from django.urls import path
from . import controller

urlpatterns = [
    path('url/register/', controller.url_register, name = 'user_url_register'),
]