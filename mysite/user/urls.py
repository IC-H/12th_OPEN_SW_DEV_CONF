from django.urls import path, include
from . import views
from .url import views as url_views

urlpatterns = [
    path('sign_in/', views.sign_in.as_view(), name='sign_in'),
    path('sign_up/', views.sign_up.as_view(), name = 'sign_up'),
    path('log_out/', views.log_out.as_view(), name = 'log_out'),
    path('check_delete/', views.CheckDelete, name = 'check_delete'),
    path('delete/', views.DeleteUser, name = 'delete'),
    path('url/', include('user.url.urls')),
]
