from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def sign_in(request):
    return render(request, 'user/sign_in.html')

def sign_up(request):
    return render(request, 'user/sign_up.html')
