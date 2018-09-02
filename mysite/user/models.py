from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(unique=True, max_length = 50)
    password = models.CharField(max_length = 32)
    created_at = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    ### DateTimeField : yyyy-mm-dd hh:mm:ss
