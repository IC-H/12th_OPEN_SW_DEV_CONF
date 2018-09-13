from django.urls import path, include
from . import views
from .url import views as url_views

urlpatterns = [
    path('sign_in/', views.sign_in.as_view(), name='sign_in'),
    path('sign_up/', views.sign_up.as_view(), name = 'sign_up'),
    path('url/', include('user.url.urls')),
]
