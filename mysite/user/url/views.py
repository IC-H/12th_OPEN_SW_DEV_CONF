from django.shortcuts import render

def register(request):
    data = {}
    return render(request, 'user/url/register.html', data)
