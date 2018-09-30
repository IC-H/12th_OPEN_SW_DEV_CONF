from common.models import HtmlVectorLite, DomainUrl
from batch.model_converter import HtmlVectorLiteModelConverter
from batch.vectorize import HtmlVectorizeLite

class VectorComparerLite():

    def __init__(self):
        self.converter = HtmlVectorLiteModelConverter()
        self.vectorizer = HtmlVectorizeLite(HtmlVectorLite.VECTOR_INDICES)

    def set_response(self, response):
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
        self.vectorizer.vectorize(query_set = HtmlVectorLite.objects.filter(url_id__exact = url_id))
        return self.vectorizer.get_vector_set()

    def compare_vector(self):
        if len(self.new_vector_set) == len(self.db_vector_set):
            for i in range(len(self.new_vector_set)):
                if self.db_vector_set[i] != self.new_vector_set[i]:
                    self.update_vector_set()
                    break
        else:
            self.update_vector_set()

    def update_vector_set(self):
        HtmlVectorLite.objects.filter(url_id__exact = self.converter.domain_url_model.pk).delete()
        self.converter.save_model_set()
        DomainUrl.objects.filter(pk__exact=self.converter.domain_url_model.pk).update(has_change = True)
