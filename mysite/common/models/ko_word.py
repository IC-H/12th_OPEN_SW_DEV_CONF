from django.db import models
from common.models import BaseWord

class KoWord(BaseWord):
    
    class Meta:
        managed = False
        db_table = 'ko_word'
