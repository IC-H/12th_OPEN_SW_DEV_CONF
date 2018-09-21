from django.db import models
from common.models import DomainUrl
from common.models import Word, Tag

class HtmlVectorLite(models.Model):
    url = models.ForeignKey(DomainUrl, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    tag_depth = models.PositiveSmallIntegerField()
     
    class Meta:
        managed = False
        db_table = 'html_vector_lite'