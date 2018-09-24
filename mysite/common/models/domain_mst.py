# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models, transaction, DatabaseError, IntegrityError
from django.core.validators import URLValidator

class DomainMst(models.Model):
    # domain is not contain scheme ex) project.oss.kr
    domain = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'domain_mst'
    
    def clean(self):
        url_with_scheme = 'https://' + self.domain
        validator = URLValidator()
        validator(url_with_scheme)
    
    def save(self, force_insert=False, force_update=False, using=None, 
        update_fields=None):
        self.clean()
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
    
    @staticmethod
    @transaction.atomic
    def find_by_domain_with_out_fail(domain):
        try:
            model = DomainMst.objects.filter(domain__exact=domain).get()
        except DomainMst.DoesNotExist:
            try:
                with transaction.atomic():
                    model = DomainMst(domain=domain)
                    model.save()
            except (DatabaseError, IntegrityError):
                # For parallel thread
                # If domain is registerd with another process search one more time
                model = DomainMst.objects.filter(domain__exact=domain).get()
        return model
