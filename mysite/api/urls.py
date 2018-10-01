from django.urls import path, include
from . import views

urlpatterns = [
    path('user/check/', views.user_check, name = 'user_check'),
    path('user/register/', views.user_register, name = 'user_register'),
    path('user/', include('api.user.urls')),
]