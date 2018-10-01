from batch.vectorize import BaseVectorize
from common.models import HtmlVector

class HtmlVectorize(BaseVectorize):
    
    class Meta:
        vector_model = HtmlVector
