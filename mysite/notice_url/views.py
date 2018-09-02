from django.shortcuts import render
from django.http import HttpResponse
from common.models.domain_url import DomainUrl

def search(request):
    domain_list = DomainUrl.find_all_with_domain()
    data = {
        'domain_list' : domain_list
    }
    return render(request, 'search/index.html', data)
