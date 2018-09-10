from django.urls import path
from . import views, ajax

urlpatterns = [
    path('search/', views.searchView.as_view(), name='search'),
    path('search/ajax/', ajax.search, name='search_ajax'),
]