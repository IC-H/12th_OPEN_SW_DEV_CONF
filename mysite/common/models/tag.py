from django.db import models

class Tag(models.Model):
    tag = models.CharField(unique=True, max_length=45)
    
    class Meta:
        managed = False
        db_table = 'tag'
