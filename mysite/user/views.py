
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .forms import AuthenticationForm, UserCreationForm
from .auth import Auth

# Create your views here.

class sign_in(LoginView):
    template_name = 'user/sign_in.html'
    form_class = AuthenticationForm
    settings.LOGIN_REDIRECT_URL = '../url/list/'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        Auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class sign_up(CreateView):
    template_name = 'user/sign_up.html'
    form_class = UserCreationForm 
    success_url = reverse_lazy('sign_in')

def url_list(request):
    return render(request, '')
