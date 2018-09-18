from django.db import models
from common.models import DomainUrl
from common.models import LangMst, BaseWord, KoWord, EnWord, Tag

class HtmlVector(models.Model):
    url = models.ForeignKey(DomainUrl, on_delete=models.CASCADE)
    lang = models.ForeignKey(LangMst, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    tag_order = models.PositiveSmallIntegerField(default=1)
    # TODO set word to multiple ForeignKey such that KoWord, EnWord etc  
    word = models.ForeignKey(BaseWord, on_delete=models.CASCADE)
    word_order = models.PositiveSmallIntegerField(default=1)
     
    class Meta:
        managed = False
        db_table = 'html_vector'
