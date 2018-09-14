from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerView.as_view(), name = 'url_register'),
    path('list/', views.UrlListView.as_view(), name = 'url_list'),
]
