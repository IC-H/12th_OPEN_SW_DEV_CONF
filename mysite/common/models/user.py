# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    email       = models.CharField(unique=True, max_length=50)
    password    = models.CharField(max_length=128)
    created_at  = models.DateTimeField()
    updated_at  = models.DateTimeField(null=True, blank=True)
    deleted_at  = models.DateTimeField(null=True, blank=True)

    class Meta(object):
        managed = False
        db_table = 'user'
