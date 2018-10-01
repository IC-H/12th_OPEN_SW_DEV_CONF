from batch.vectorize import BaseVectorize
from common.models import HtmlVectorWithDepth

class HtmlDepthVectorizor(BaseVectorize):
    
    class Meta:
        vector_model = HtmlVectorWithDepth
