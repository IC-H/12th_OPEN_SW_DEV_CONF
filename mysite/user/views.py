from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .forms import AuthenticationForm, UserCreationForm

# Create your views here.

class sign_in(LoginView):
    template_name = 'user/sign_in.html'
    form_class = AuthenticationForm
    settings.LOGIN_REDIRECT_URL = '../url/list/'

class sign_up(CreateView):
    template_name = 'user/sign_up.html'
    form_class = UserCreationForm 
    success_url = reverse_lazy('sign_in')
