# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from common.models.domain_mst import DomainMst

class DomainUrl(models.Model):
    domain  = models.ForeignKey(DomainMst, on_delete=models.CASCADE)
    url     = models.CharField(max_length=255)

    @staticmethod
    def find_all_with_domain_contains_keywords(domain_key='', url_key='', connector='OR'):
        # Validate input type
        if not isinstance(domain_key, str):
            raise TypeError('domain_key has to be string')
        if not isinstance(url_key, str):
            raise TypeError('url_key has to be string')
        if connector not in ['AND', 'OR']:
            raise TypeError('connector has to be "AND" OR "OR"')
        
        domain_obj_list = DomainUrl.objects.all().select_related()
        Q_list          = []
        if domain_key != '':
            Q_list.append(models.Q(domain__domain__contains=domain_key))
            
        if url_key != '':
            Q_list.append(models.Q(url__contains=url_key))
        
        if len(Q_list) > 0:
            Q_factor = models.Q()
            for Q in Q_list:
                Q_factor = Q_factor._combine(Q, connector)
            domain_obj_list = domain_obj_list.filter(Q_factor)
        
        return domain_obj_list

    @staticmethod
    def find_all_with_domain(key_word=''):
        # Validate input type
        if not isinstance(key_word, str):
            raise TypeError('key_word has to be string')
        
        domain_list     = {}
        domain_obj_list = DomainUrl.find_all_with_domain_contains_keywords(key_word, key_word)
        
        for obj in domain_obj_list:
            if obj.domain_id in domain_list:
                domain_list[obj.domain_id]['url_list'].append(obj.url)
            else:
                domain_list[obj.domain_id] = {
                    'domain'    : obj.domain.domain,
                    'url_list'  : [obj.url]
                }
                
        return domain_list

    class Meta:
        managed = False
        db_table = 'domain_url'
