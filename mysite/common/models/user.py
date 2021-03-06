# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.utils.crypto import salted_hmac


class User(models.Model):
    email       = models.CharField(unique=True, max_length=50)
    password    = models.CharField(max_length=128)
    created_at  = models.DateTimeField()
    updated_at  = models.DateTimeField(null=True)
    deleted_at  = models.DateTimeField(null=True)

    EMAIL_FIELD = 'email'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_datetime(self):
        self.created_at = datetime.now()

    def get_session_auth_hash(self):
        key_salt = settings.KEY_SALT
        return salted_hmac(key_salt, self.password).hexdigest()

    class Meta(object):
        managed = False
        db_table = 'user'
