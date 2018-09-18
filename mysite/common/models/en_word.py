from django.db import models
from common.models import BaseWord

class EnWord(BaseWord):
    
    class Meta:
        managed = False
        db_table = 'en_word'
