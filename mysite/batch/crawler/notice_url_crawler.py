from threading import Thread
from .base_crawler import BaseCrawler
from batch.navigator import Navigator
from batch.model_converter import HtmlVectorModelConverter
from batch.vectorize import HtmlVectorize
from common.models import DomainUrl, HtmlVector
from datetime import datetime

class NoticeUrlCrawler(BaseCrawler, Thread):
    
    count = []
    
    def __init__(self, *args, **kwargs):
        crawler_kwargs = {}
        protocol = kwargs.pop('protocol',None)
        if protocol is not None:
            crawler_kwargs['protocol'] = protocol
        BaseCrawler.__init__(self, *args, **crawler_kwargs)
        Thread.__init__(self, *args, **kwargs)
        self.navigator = Navigator()
        self.count.append(1)
        self.start_time = datetime.now()
        print('crawler init %s' % len(self.count))
    
    def run(self):
        converter = HtmlVectorModelConverter()
        vectorizor = HtmlVectorize(HtmlVector.VECTOR_INDICES)
        
        while not self.navigator.is_over():
            tmp = datetime.now()
            url, request_moethod, request_params = self.navigator.get_next()
            print('get next over %s second' % (datetime.now() - tmp).total_seconds())
            response = None
            if request_moethod == 'POST':
                response = self.post_request(url, request_params)
            elif request_moethod == 'GET':
                response = self.get_request(url)
            
            tmp = datetime.now()
            self.navigator.analyze_response(response)
            print('analyze_response over %s second' % (datetime.now() - tmp).total_seconds())
            if response is None:
                continue
            
            if DomainUrl.objects.filter(url__exact=url).exists():
                continue
            
            tmp = datetime.now()
            converter.run(response)
            print('converter over %s second' % (datetime.now() - tmp).total_seconds())
            converter.save_model_set()
            tmp = datetime.now()
            vectorizor.reset_vector_set()
            for model in converter.vector_model_set:
                vectorizor.vectorize(model)
            vector_set = vectorizor.get_vector_set
            print('vectorize over %s second' % (datetime.now() - tmp).total_seconds())
            '''
            check that url is for notice or not using vector_set
            '''
    
    def __del__(self):
        self.count.pop(0)
        end_time = datetime.now()
        print('crawler del %s' % len(self.count))
        #print('crawler run over %s second' % (end_time - self.start_time).total_seconds())
