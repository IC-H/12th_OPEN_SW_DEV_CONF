from . import BaseCrawler
from common.models import DomainUrl
from batch.compare_vector import VectorComparerLite

class NoticeCrawlerLite(BaseCrawler):

    def find_notice_model(self):
        return DomainUrl.objects.filter(is_notice__exact = True)

    def run(self):
        Comparer = VectorComparerLite()
        for model in self.find_notice_model():
            response = self.get_request(model.url)
            Comparer.set_response(response)
            Comparer.compare_vector()
