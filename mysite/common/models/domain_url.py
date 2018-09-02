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

    def find_all_with_domain():
        domain_list = []
        for domain_data in DomainMst.objects.all():
            url_list = []
            for url_data in DomainUrl.objects.filter(domain__exact=domain_data.id):
                url_list.append(url_data.url)
            data = {
                'domain'    : domain_data.domain,
                'url_list'  : url_list
            }
            domain_list.append(data)
        return domain_list

    class Meta:
        managed = False
        db_table = 'domain_url'
