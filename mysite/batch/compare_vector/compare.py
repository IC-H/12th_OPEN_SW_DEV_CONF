from common.models import DomainUrl, HtmlVector
from batch.vectorize import HtmlVectorize

class CompareVector():

    def __init__(self, vector_model_set):
        self.indeces = ['url_id', 'lang_id', 'tag_id', 'tag_order', 'word_id', 'word_order']
        self.vector_model_set = vector_model_set
        self.new_model = self.get_vector_from_html()
        self.db_model = self.get_vector_from_db()

    def get_vector_from_html(self):
        vectorizer = HtmlVectorize(self.indeces)
        for _model in self.vector_model_set:
            vectorizer.vectorize(_model)
        return vectorizer.get_vector_set()

    def get_url_id(self):
        return self.new_model[0][0]

    def get_vector_from_db(self):
        url_id = self.get_url_id()
        vectorizer = HtmlVectorize(self.indeces)
        for _model in HtmlVector.objects.filter(url_id__exact = url_id):
            vectorizer.vectorize(_model)
        return vectorizer.get_vector_set()

    def compare_vector(self):
        if len(self.db_model) == 0:
            self.save()
            print('save')
        elif len(self.new_model) == len(self.db_model):
            for i in range(len(self.new_model)):
                if Com.db_model[i] != Com.new_model[i]:
                    self.save()
        else:
        	self.save()
                   
    def update(self):
        DomainUrl.objects.filter(pk__exact = self.get_url_id()).update(has_change = True)

    def save(self):
        for _model in self.vector_model_set:
            _model.save()
        self.update()

