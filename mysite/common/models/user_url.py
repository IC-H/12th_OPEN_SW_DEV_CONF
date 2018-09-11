# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from common.models import User, DomainUrl
from django.core.exceptions import ValidationError
from copy import copy

class UserUrl(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    url     = models.ForeignKey(DomainUrl, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'user_url'
        unique_together = (('user', 'url'),)
    
    @staticmethod
    def get_diff_from_user_choices(user_id, url_id_list):
        try:
            # validate and make user_id's type integer
            user_id = int(user_id)
        except TypeError:
            raise ValidationError('user_id has to be numerous')
        try:
            # validate and make url_id's type integer
            url_id_list = {index : int(url_id) for index, url_id in enumerate(url_id_list)} if len(url_id_list) > 0 else {}
        except TypeError:
            raise ValidationError('url_id_list has to be list with numerous items')
        
        current_registered_query_set = UserUrl.objects.filter(user__id__exact=user_id)
        # data list will be added
        added_data      = {}
        # data list will be deleted
        deleted_data    = {}
        
        current_registered_data_list    = {}
        for user_url_obj in current_registered_query_set:
            current_registered_data_list[user_url_obj.url_id] = user_url_obj
        
        for index, url_id in copy(url_id_list).items():
            if url_id in current_registered_data_list.keys():
                # delete item which has not changed
                del url_id_list[index]
                del current_registered_data_list[url_id]
        
        added_query_set = DomainUrl.objects.filter(pk__in=url_id_list).select_related()
        deleted_query_set = DomainUrl.objects.filter(pk__in=current_registered_data_list.keys()).select_related()
        
        return {
            'added_domain_list'     : DomainUrl.get_dict_type_domain_url_list(added_query_set),
            'deleted_domain_list'   : DomainUrl.get_dict_type_domain_url_list(deleted_query_set)
        }
