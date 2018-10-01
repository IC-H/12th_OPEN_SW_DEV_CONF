from django.db import models
from common.models import DomainUrl
from common.models import Tag

class HtmlVectorLite(models.Model):
    url = models.ForeignKey(DomainUrl, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    tag_order = models.PositiveSmallIntegerField(default=1)
    depth = models.PositiveSmallIntegerField(default=1)
    
    VECTOR_INDICES = ['tag_id', 'tag_order', 'depth']
    
    class Meta:
        managed = False
        db_table = 'html_vector_lite'
