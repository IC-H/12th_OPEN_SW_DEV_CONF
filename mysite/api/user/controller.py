from django.shortcuts import redirect
from django.urls import reverse_lazy
from common.models import User

def url_register(request):
    
    return redirect(reverse_lazy('search'))