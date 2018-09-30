from common.models import HtmlVector, DomainUrl
from batch.model_converter import HtmlVectorModelConverter
from batch.vectorize import HtmlVectorize

class VectorComparer():

    def __init__(self):
        self.converter = HtmlVectorModelConverter()
        self.vectorizer = HtmlVectorize(HtmlVector.VECTOR_INDICES)

    def set_response(self, response):
        print(response.url)
        self.converter.run(response)
        self.new_vector_set = self.get_vector_from_html()
        self.db_vector_set = self.get_vector_from_db()

    def get_vector_from_html(self):
        self.vectorizer.reset_vector_set()
        for _model in self.converter.vector_model_set:
            self.vectorizer.vectorize(_model)
        return self.vectorizer.get_vector_set()

    def get_vector_from_db(self):
        self.vectorizer.reset_vector_set()
        url_id = self.converter.domain_url_model.pk
        self.vectorizer.vectorize(query_set = HtmlVector.objects.filter(url_id__exact = url_id))
        return self.vectorizer.get_vector_set()

    def compare_vector(self):
        print(len(self.new_vector_set), len(self.db_vector_set))
        print('len of new vector set %s' % len(self.new_vector_set))
        print('len of db vector set %s' % len(self.db_vector_set))
        if len(self.new_vector_set) == len(self.db_vector_set):
            for i in range(len(self.new_vector_set)):
                if self.db_vector_set[i] != self.new_vector_set[i]:
                    self.update_vector_set()
                    break
        else:
            self.update_vector_set()

    def update_vector_set(self):
        print('-- save --')
        HtmlVector.objects.filter(url_id__exact = self.converter.domain_url_model.pk).delete()    	
        self.converter.save_model_set()
        DomainUrl.objects.filter(pk__exact=self.converter.domain_url_model.pk).update(has_change = True)

