from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import DatabaseError, IntegrityError, transaction
from common.models import User, UserUrl, DomainUrl
from user.auth import Auth

@transaction.atomic
def url_register(request):
    if request.method != 'POST':
        messages.add_message(request, messages.ERROR, 'BAD REQUESTS!!')
        return redirect(reverse_lazy('search'))
    user = Auth.get_user(request)
    added_url_id_list   = request.POST.getlist('added_url_id_list[]')
    deleted_url_id_list = request.POST.getlist('deleted_url_id_list[]')
    try:
        with transaction.atomic():
            if len(added_url_id_list) > 0:
                for url_obj in DomainUrl.objects.filter(pk__in=added_url_id_list):
                    user_url_obj = UserUrl(
                        user=user,
                        url=url_obj
                    ).save()
            if len(deleted_url_id_list) > 0:
                UserUrl.objects.filter(user__id__exact=user.id).filter(url__id__in=deleted_url_id_list).delete()
    except (Exception) as e:
        messages.add_message(request, messages.ERROR, e)
        return redirect(reverse_lazy('search'))
    
    messages.add_message(request, messages.SUCCESS, 'Success for saving')
    return redirect(reverse_lazy('url_list'))
