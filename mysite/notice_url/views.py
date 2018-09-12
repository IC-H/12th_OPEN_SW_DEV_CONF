from django.views.generic.list import ListView
from common.models.domain_url import DomainUrl

class searchView(ListView):
    template_name = 'search/index.html'
    context_object_name = 'domain_list'
    
    def get_queryset(self):
        return DomainUrl.find_all_with_domain()
