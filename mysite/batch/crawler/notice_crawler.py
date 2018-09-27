from . import BaseCrawler
from common.models import DomainUrl, HtmlVector
from batch.compare_vector import VectorComparer

class NoticeCrawler(BaseCrawler):

    def find_notice_model(self):
        return DomainUrl.objects.filter(is_notice__exact = True)

    def run(self):
        Comparer = VectorComparer()
        for model in self.find_notice_model():
        	response = self.get_request(model.url)
        	Comparer.set_response(response)
        	Comparer.compare_vector()
