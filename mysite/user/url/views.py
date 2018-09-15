from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from common.models import User, UserUrl, DomainUrl

class registerView(ListView):
    template_name = 'user/url/register.html'
    
    def get_queryset(self):
        try:
            user_pk = int(self.request.session['_auth_email_id'])
            user = User(pk=user_pk)
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Please Log In')
            return redirect(reverse_lazy('sign_in')) 
        url_id_list = self.request.POST.getlist('url_id_list[]')
        query_set_list = UserUrl.get_diff_query_set_from_user_choices(user.id, url_id_list)
        return {
            'added_domain_list'     : DomainUrl.get_dict_type_domain_url_list(query_set_list['added_query_set']),
            'deleted_domain_list'   : DomainUrl.get_dict_type_domain_url_list(query_set_list['deleted_query_set'])
        }

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)

class UrlListView(ListView):
    template_name = 'user/url/list.html'
    
    def dispatch(self, request, *args, **kwargs):
        try:
            user_pk = int(request.session['_auth_email_id'])
            user = User.objects.filter(pk__exact=user_pk).get()
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Please Log In')
            return redirect(reverse_lazy('sign_in'))
        self.user = user
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user_url_query_set  = UserUrl.objects.filter(user__id__exact=self.user.id)
        url_id_list         = [obj.url_id for obj in user_url_query_set]
        query_set_list      = DomainUrl.objects.filter(pk__in=url_id_list).select_related()
        
        return {
            'domain_list' : DomainUrl.get_dict_type_domain_url_list(query_set_list)
        }
