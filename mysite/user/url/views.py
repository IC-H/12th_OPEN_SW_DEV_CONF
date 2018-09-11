from django.views.generic.list import ListView
from common.models import User, UserUrl

class registerView(ListView):
    template_name = 'user/url/register.html'
    
    def get_queryset(self):
        url_id_list = self.request.POST.getlist('url_id_list[]')
        data = {
            'added_domain_list' : {
                2 : {
                    'domain'    : 'www.cau.ac.kr',
                    'url_list'  : {
                        3 : "www.cau.ac.kr/01_intro/status/status10_list.php"
                    },
                },
            },
            'deleted_domain_list' : {
                2 : {
                    'domain'    : 'www.cau.ac.kr',
                    'url_list'  : {
                        2 : "www.cau.ac.kr/04_ulife/causquare/notice/notice_list.php",
                    },
                },
            }
        }
        return data

    def post(self, request, *args, **kwargs):
        return self.get(self, request, *args, **kwargs)
