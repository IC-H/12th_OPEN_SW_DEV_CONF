from common.models import HtmlVector
### from batch.model_converter import HtmlVectorModelConverter
from batch.vectorize import HtmlVectorize

class CompareVector():

    def __init__(self, vector_model_set):
    	self.indeces = ['url_id', 'lang_id', 'tag_id', 'tag_order', 'word_id', 'word_order']
        self.new_model = self.get_vector_from_html(vector_model_set)
        self.db_model = self.get_vector_from_db(url_id)

    def get_vector_from_html(self, vector_model_set):
        vectorizer = HtmlVectorize(self.indeces)
        for _model in vector_model_set:
            vectorizer.vectorize(_model)
        return vectorizer.get_vector_set()

    def get_vector_from_db(self, url_id):
        vectorizer = HtmlVectorize(self.indeces)
        for _model in HtmlVector.objects.filter(url_id__exact = 13):
            vectorizer.vectorize(_model)
        return vectorizer.get_vector_set()

    def compare_vector:
    	pass

    def save:
    	pass
