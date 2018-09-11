from django.views.generic.list import ListView
from common.models import User, UserUrl

class registerView(ListView):
    template_name = 'user/url/register.html'
    
    def get_queryset(self):
        # TODO log-in function
        user = User(pk=1)
        url_id_list = self.request.POST.getlist('url_id_list[]')
        data = UserUrl.get_diff_from_user_choices(user.id, url_id_list)
        return data

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)
