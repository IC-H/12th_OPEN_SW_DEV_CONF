from django.db import models
from common.models import DomainUrl, LangMst, Word, Tag

class HtmlVectorWithDepth(models.Model):
    url = models.ForeignKey(DomainUrl, on_delete=models.CASCADE)
    lang = models.ForeignKey(LangMst, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    tag_order = models.PositiveSmallIntegerField(default=1)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    word_order = models.PositiveSmallIntegerField(default=1)
    depth = models.PositiveSmallIntegerField(default=1)
    
    VECTOR_INDICES = ['lang_id', 'tag_id', 'tag_order', 'word_id', 'word_order', 'depth']
    
    class Meta:
        managed = False
        db_table = 'html_vector_with_depth'
