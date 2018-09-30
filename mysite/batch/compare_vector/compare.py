from common.models import DomainUrl, HtmlVector, HtmlVectorWithDepth, HtmlVectorLite
from batch.model_converter import HtmlVectorModelConverter, HtmlVectorWithDepthModelConverter, HtmlVectorLiteModelConverter
from batch.vectorize import HtmlVectorize, HtmlDepthVectorizor, HtmlVectorizeLite

class VectorComparer():

    def __init__(self):
        # convert request.models.Response to each model of vector
        self.converter = HtmlVectorModelConverter()
        self.depth_converter = HtmlVectorWithDepthModelConverter()
        self.lite_converter = HtmlVectorLiteModelConverter()
        # vectorizor for each model of vector
        self.vectorizer = HtmlVectorize(HtmlVector.VECTOR_INDICES)
        self.depth_vectorizer = HtmlDepthVectorizor(HtmlVectorWithDepth.VECTOR_INDICES)
        self.lite_vectorizer = HtmlVectorizeLite(HtmlVectorLite.VECTOR_INDICES)
        # vector set from html
        self.new_vector_set = []
        self.new_depth_vector_set = []
        self.new_lite_vector_set = []
        # vector set from db
        self.db_vector_set = []
        self.db_depth_vector_set = []
        self.db_lite_vector_set = []
    
    def run_converter(self, response):
        self.converter.run(response)
        self.depth_converter.run(response)
        self.lite_converter.run(response)
    
    def set_response(self, response):
        self.run_converter(response)
        self.set_vector_from_html()
        self.set_vector_from_db()
    
    def _set_vector_from_html(self):
        self.vectorizer.reset_vector_set()
        for _model in self.converter.vector_model_set:
            self.vectorizer.vectorize(_model)
        self.new_vector_set = self.vectorizer.get_vector_set()
    
    def _set_depth_vector_from_html(self):
        self.depth_vectorizer.reset_vector_set()
        for _model in self.depth_converter.vector_model_set:
            self.depth_vectorizer.vectorize(_model)
        self.new_depth_vector_set =self.depth_vectorizer.get_vector_set()
    
    def _set_lite_vector_from_html(self):
        self.lite_vectorizer.reset_vector_set()
        for _model in self.lite_converter.vector_model_set:
            self.lite_vectorizer.vectorize(_model)
        self.new_lite_vector_set =self.lite_vectorizer.get_vector_set()
    
    def set_vector_from_html(self):
        self._set_vector_from_html()
        self._set_depth_vector_from_html()
        self._set_lite_vector_from_html()
    
    def _set_vector_from_db(self):
        self.vectorizer.reset_vector_set()
        self.vectorizer.vectorize(query_set = HtmlVector.objects.filter(url__exact=self.converter.domain_url_model))
        self.db_vector_set = self.vectorizer.get_vector_set()
    
    def _set_depth_vector_from_db(self):
        self.depth_vectorizer.reset_vector_set()
        self.depth_vectorizer.vectorize(query_set = HtmlVectorWithDepth.objects.filter(url__exact=self.depth_converter.domain_url_model))
        self.db_depth_vector_set = self.depth_vectorizer.get_vector_set()
    
    def _set_lite_vector_from_db(self):
        self.lite_vectorizer.reset_vector_set()
        self.lite_vectorizer.vectorize(query_set = HtmlVectorLite.objects.filter(url__exact = self.lite_converter.domain_url_model))
        self.db_lite_vector_set = self.lite_vectorizer.get_vector_set()
    
    def set_vector_from_db(self):
        self._set_vector_from_db()
        self._set_depth_vector_from_db()
        self._set_lite_vector_from_db()
    
    def compare_vector(self):
        print(len(self.new_vector_set), len(self.db_vector_set))
        print('len of new vector set %s' % len(self.new_vector_set))
        print('len of db vector set %s' % len(self.db_vector_set))
        # for html_vector
        if len(self.new_vector_set) == len(self.db_vector_set):
            for i in range(len(self.new_vector_set)):
                if self.db_vector_set[i] != self.new_vector_set[i]:
                    self.update_vector_set()
                    break
        else:
            self.update_vector_set()
        # for html_vector_with_depth
        if len(self.new_depth_vector_set) == len(self.db_depth_vector_set):
            for i in range(len(self.new_depth_vector_set)):
                if self.db_depth_vector_set[i] != self.new_depth_vector_set[i]:
                    self.update_depth_vector_set()
                    break
        else:
            self.update_depth_vector_set()
        # for html_vector_lite
        if len(self.new_lite_vector_set) == len(self.db_lite_vector_set):
            for i in range(len(self.new_lite_vector_set)):
                if self.db_lite_vector_set[i] != self.new_lite_vector_set[i]:
                    self.update_lite_vector_set()
                    break
        else:
            self.update_lite_vector_set()

    def update_vector_set(self):
        print('-- save --')
        HtmlVector.objects.filter(url_id__exact = self.converter.domain_url_model.pk).delete()    	
        self.converter.save_model_set()
        self.converter.domain_url_model.has_change = True
        self.converter.domain_url_model.save()
    
    def update_depth_vector_set(self):
        print('-- save --')
        HtmlVectorWithDepth.objects.filter(url__exact = self.depth_converter.domain_url_model).delete()        
        self.depth_converter.save_model_set()
        self.depth_converter.domain_url_model.has_change = True
        self.depth_converter.domain_url_model.save()
    
    def update_lite_vector_set(self):
        print('-- save --')
        HtmlVectorLite.objects.filter(url__exact = self.lite_converter.domain_url_model).delete()        
        self.lite_converter.save_model_set()
        self.lite_converter.domain_url_model.has_change = True
        self.lite_converter.domain_url_model.save()
