from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth import REDIRECT_FIELD_NAME
from urllib.parse import urlparse, urlunparse
from .forms import AuthenticationForm, UserCreationForm
from .auth import Auth
from datetime import datetime

# Create your views here.

class sign_in(LoginView):
    template_name = 'user/sign_in.html'
    form_class = AuthenticationForm
    settings.LOGIN_REDIRECT_URL = reverse_lazy('url_list')

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        Auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class sign_up(CreateView):
    template_name = 'user/sign_up.html'
    form_class = UserCreationForm 
    success_url = reverse_lazy('sign_in')

def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirect the user to the login page, passing the given 'next' page.
    """
    resolved_url = resolve_url(login_url or reverse_lazy('sign_in'))

    login_url_parts = list(urlparse(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe='/')

    return HttpResponseRedirect(urlunparse(login_url_parts))


class log_out(LogoutView):
    template_name = 'user/log_out.html'


def CheckDelete(request):
    return render(request, 'user/check_delete.html')


def DeleteUser(request):
    user = Auth.get_user(request)
    user.updated_at = datetime.now()
    user.deleted_at = datetime.now()
    user.save()
    return render(request, 'user/delete.html')
