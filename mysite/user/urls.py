from django.urls import path
from . import views
from .url import views as url_views

urlpatterns = [
    path('sign_in/', views.sign_in, name = 'sign_in'),
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('url/register/', url_views.register, name = 'url_register'),
]
