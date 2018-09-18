from django.db import models

class BaseWord(models.Model):
    word = models.CharField(unique=True, max_length=45)
    
    class Meta:
        managed = False
