from threading import Thread
from .base_crawler import BaseCrawler
from batch.navigator import Navigator
from batch.model_converter import HtmlVectorModelConverter, HtmlVectorWithDepthModelConverter, HtmlVectorLiteModelConverter
from batch.vectorize import HtmlVectorize, HtmlDepthVectorizor, HtmlVectorizeLite
from common.models import DomainUrl, HtmlVector, HtmlVectorWithDepth, HtmlVectorLite
from batch.learning import SvmClassifier
from requests.exceptions import Timeout

class NoticeUrlCrawler(BaseCrawler, Thread):
    
    def __init__(self, *args, **kwargs):
        crawler_kwargs = {}
        protocol = kwargs.pop('protocol',None)
        if protocol is not None:
            crawler_kwargs['protocol'] = protocol
        BaseCrawler.__init__(self, *args, **crawler_kwargs)
        Thread.__init__(self, *args, **kwargs)
        self.navigator = Navigator()
        self.classifier = SvmClassifier()
    
    def run(self):
        # convert request.models.Response to each model of vector
        converter = HtmlVectorModelConverter()
        depth_converter = HtmlVectorWithDepthModelConverter()
        lite_converter = HtmlVectorLiteModelConverter()
        # vectorizor for each model of vector
        vectorizor = HtmlVectorize(HtmlVector.VECTOR_INDICES)
        depth_vectorizor = HtmlDepthVectorizor(HtmlVectorWithDepth.VECTOR_INDICES)
        lite_vectorizor = HtmlVectorizeLite(HtmlVectorLite.VECTOR_INDICES)
        
        while not self.navigator.is_over():
            url, request_moethod, request_params = self.navigator.get_next()
            response = None
            try:
                if request_moethod == 'POST':
                    response = self.post_request(url, request_params)
                elif request_moethod == 'GET':
                    response = self.get_request(url)
            except Timeout as e:
                print(e)
                continue
            
            self.navigator.analyze_response(response)
            if response is None:
                continue
            
            if DomainUrl.objects.filter(url__exact=url).exists():
                continue
            
            converter.run(response)
            depth_converter.run(response)
            lite_converter.run(response)
            converter.save_model_set()
            depth_converter.save_model_set()
            lite_converter.save_model_set()
            vectorizor.reset_vector_set()
            for model in converter.vector_model_set:
                vectorizor.vectorize(model)
            vector_set = vectorizor.get_vector_set
            depth_vectorizor.reset_vector_set()
            for model in depth_converter.vector_model_set:
                depth_vectorizor.vectorize(model)
            depth_vector_set = depth_vectorizor.get_vector_set
            lite_vectorizor.reset_vector_set()
            for model in lite_converter.vector_model_set:
                lite_vectorizor.vectorize(model)
            lite_vector_set = lite_vectorizor.get_vector_set
            if not self.classifier.did_learn:
                is_notice = self.classifier(vector_set)
                converter.domain_url_model.is_notice = is_notice
                converter.domain_url_model.save()
