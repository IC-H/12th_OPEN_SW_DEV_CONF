from django.http import JsonResponse
from common.models.domain_url import DomainUrl

def search(request):
    key_word    = request.POST.get('keyWrods', '')
    results     = DomainUrl.find_all_with_domain(key_word)
    
    data = {
        'domain_list' : results
    }
    return JsonResponse(data)
