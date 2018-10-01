from batch.vectorize import BaseVectorize
from common.models import HtmlVectorLite

class HtmlVectorizeLite(BaseVectorize):
    
    class Meta:
        vector_model = HtmlVectorLite
