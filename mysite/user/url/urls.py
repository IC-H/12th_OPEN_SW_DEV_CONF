from django.urls import path
from . import views

urlpatterns = [
    path('url/register/', views.registerView.as_view(), name = 'url_register'),
    path('url/list/', views.UrlListView.as_view(), name = 'url_list'),
]
