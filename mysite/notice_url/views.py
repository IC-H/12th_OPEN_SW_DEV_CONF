from django.shortcuts import render
from django.http import HttpResponse

def search(request):
    return HttpResponse("Hello, world. You're at the notice_url search.")