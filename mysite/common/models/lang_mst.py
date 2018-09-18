from django.db import models

class LangMst(models.Model):
    language = models.CharField(unique=True, max_length=45)
    
    class Meta:
        managed = False
        db_table = 'lang_mst'
