from django.views.generic.list import ListView
from common.models import User, UserUrl, DomainUrl

class registerView(ListView):
    template_name = 'user/url/register.html'
    
    def get_queryset(self):
        # TODO log-in function
        user = User(pk=1)
        url_id_list = self.request.POST.getlist('url_id_list[]')
        query_set_list = UserUrl.get_diff_query_set_from_user_choices(user.id, url_id_list)
        return {
            'added_domain_list'     : DomainUrl.get_dict_type_domain_url_list(query_set_list['added_query_set']),
            'deleted_domain_list'   : DomainUrl.get_dict_type_domain_url_list(query_set_list['deleted_query_set'])
        }

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)
