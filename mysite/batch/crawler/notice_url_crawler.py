from threading import Thread
from .base_crawler import BaseCrawler
from batch.navigator import Navigator
from batch.model_converter import HtmlVectorModelConverter
from batch.vectorize import HtmlVectorize
from common.models import DomainUrl, HtmlVector

class NoticeUrlCrawler(BaseCrawler, Thread):
    
    def __init__(self, *args, **kwargs):
        BaseCrawler.__init__(self, *args, **kwargs)
        Thread.__init__(self, *args, **kwargs)
        self.navigator = Navigator()
    
    def run(self):
        converter = HtmlVectorModelConverter()
        vectorizor = HtmlVectorize(HtmlVector.VECTOR_INDICES)
        
        while not self.navigator.is_over():
            url, request_moethod, request_params = self.navigator.get_next()
            response = None
            if request_moethod == 'POST':
                response = self.post_request(url, request_params)
            elif request_moethod == 'GET':
                response = self.get_request(url)
            
            self.navigator.analyze_response(response)
            
            if response is None:
                continue
            
            if DomainUrl.objects.filter(url__exact=url).exists():
                continue
            
            converter.run(response)
            converter.save_model_set()
            vectorizor.reset_vector_set()
            for model in converter.vector_model_set:
                vectorizor.vectorize(model)
            vector_set = vectorizor.get_vector_set
            '''
            check that url is for notice or not using vector_set
            '''
