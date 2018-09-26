from common.models import DomainUrl, HtmlVector
from batch.model_converter import HtmlVectorModelConverter
from batch.vectorize import HtmlVectorize

class VectorComparer():

    def __init__(self, response):
        self.indices = ['url_id', 'lang_id', 'tag_id', 'tag_order', 'word_id', 'word_order']
        self.initialize(response)

    def initialize(self, response):
        self.converter = self.set_converter(response)
        self.new_vector_set = self.get_vector_from_html()
        self.db_vector_set = self.get_vector_from_db()

    def set_converter(self, response):
        converter = HtmlVectorModelConverter()
        converter.run(response)
        return converter

    def get_vector_from_html(self):
        vectorizer = HtmlVectorize(self.indices)
        for _model in self.converter.vector_model_set:
            vectorizer.vectorize(_model)
        return vectorizer.get_vector_set()

    def get_vector_from_db(self):
        url_id = self.converter.domain_url_model.pk
        vectorizer = HtmlVectorize(self.indices)
        for _model in HtmlVector.objects.filter(url_id__exact = url_id):
            vectorizer.vectorize(_model)
        return vectorizer.get_vector_set()

    def compare_vector(self):
        if len(self.new_vector_set) == len(self.db_vector_set):
            for i in range(len(self.new_vector_set)):
                if self.db_vector_set[i] != self.new_vector_set[i]:
                    self.update_new_vector()
                    break
        else:
            self.update_new_vector()

    def update_new_vector(self):
        HtmlVector.objects.filter(url_id__exact = self.converter.domain_url_model.pk).delete()    	
        self.converter.save_model_set()
        self.converter.domain_url_model.update(has_change = True)

