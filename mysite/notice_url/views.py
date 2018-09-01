from django.shortcuts import render
from django.http import HttpResponse

def search(request):
    data = {
        'domain_list' : [
            {
                'domain'    : 'domain1',
                'url_list'  : ['url1', 'url2']
            },
            {
                'domain'    : 'domain2',
                'url_list'  : ['url1']
            }
        ]
    }
    return render(request, 'search/index.html', data);