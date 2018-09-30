from . import BaseCrawler
from common.models import DomainUrl
from batch.compare_vector import VectorComparer
import requests

class NoticeCrawler(BaseCrawler):

    def find_notice_model(self):
        return DomainUrl.objects.filter(is_notice__exact = True)

    def run(self):
        Comparer = VectorComparer()
        for model in self.find_notice_model():
            try:
                response = self.get_request(model.url)
                print(model.url)
            except requests.exceptions.Timeout as e:
                print(e)
                continue
            except Exception as e:
                print(e)
                continue
            Comparer.set_response(response)
            Comparer.compare_vector()
