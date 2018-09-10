# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from common.models.user import User
from common.models.domain_url import DomainUrl

class UserUrl(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    url     = models.ForeignKey(DomainUrl, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'user_url'
        unique_together = (('user', 'url'),)
