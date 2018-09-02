from django.urls import path
from . import views

urlpatterns = [
    path('user/check/', views.user_check, name = 'user_check'),
    path('user/register/', views.user_register	, name = 'user_register'),
    path('user/url/register/', views.user_url_register, name = 'user_url_register'),
]