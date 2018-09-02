from django.db import models

# Create your models here.
class User(models.Model):
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 32)
    created_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    ### DateTimeField : yyyy-mm-dd hh:mm:ss
