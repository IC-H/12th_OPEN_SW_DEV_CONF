# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models, transaction, DatabaseError, IntegrityError
from common.models import DomainMst
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import re

class DomainUrl(models.Model):
    domain      = models.ForeignKey(DomainMst, on_delete=models.CASCADE)
    # url is not contain scheme ex) project.oss.kr/index.do
    url         = models.CharField(max_length=255)
    is_notice   = models.BooleanField(default=0, db_index=True)
    has_change  = models.BooleanField(default=0, db_index=True)

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
    def get_dict_type_domain_url_list(query_set):
        if not isinstance(query_set, models.QuerySet):
            raise TypeError('query_set has to be instance of QuerySet')
        try:
            domain_list     = {}
            for obj in query_set:
                if obj.domain_id in domain_list:
                    domain_list[obj.domain_id]['url_list'][obj.id] = obj.url
                else:
                    domain_list[obj.domain_id] = {
                        'domain'    : obj.domain.domain,
                        'url_list'  : {obj.id : obj.url}
                    }
        except (AttributeError, TypeError):
            raise ValidationError('query_set has to be QuerySet with DomainUrl instances')
                
        return domain_list

    @staticmethod
    def find_all_with_domain(key_word=''):
        # Validate input type
        if not isinstance(key_word, str):
            raise TypeError('key_word has to be string')
        
        domain_query_set = DomainUrl.find_all_with_domain_contains_keywords(key_word, key_word)
                
        return DomainUrl.get_dict_type_domain_url_list(domain_query_set)

    class Meta:
        managed = False
        db_table = 'domain_url'
        indexes = [
            models.Index(fields=['is_notice'], name='is_notice_idx'),
            models.Index(fields=['has_change'], name='has_change_idx'),
        ]
    
    def clean(self):
        url_with_scheme = 'https://' + self.url
        validator = URLValidator()
        validator(url_with_scheme)
    
    def save(self, force_insert=False, force_update=False, using=None, 
        update_fields=None):
        self.clean()
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
    
    @staticmethod
    @transaction.atomic
    def find_by_url_with_out_fail(url):
        try:
            model = DomainUrl.objects.filter(url__exact=url).get()
        except DomainUrl.DoesNotExist:
            try:
                with transaction.atomic():
                    domain = re.search(r'^[^\/]*', url).group()
                    domain_model = DomainMst.find_by_domain_with_out_fail(domain)
                    model = DomainUrl(domain=domain_model, url=url)
                    model.save()
            except (DatabaseError, IntegrityError):
                # For parallel thread
                # If domain is registerd with another process search one more time
                model = DomainUrl.objects.filter(url__exact=url).get()
        return model
