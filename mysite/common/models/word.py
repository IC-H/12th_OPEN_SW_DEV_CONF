from django.db import models
from common.models import LangMst

class Word(models.Model):
    word = models.CharField(unique=True, max_length=45)
    lang = models.ForeignKey(LangMst, on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'word'
