from common.models import DomainUrl
from .base_data_maker import BaseDataMaker
import re

class NoticeUrlDataMaker(BaseDataMaker):
    
    class Meta:
        question = 'Is url for notice ? Y or N  :  '
    
    def gather_data_set(self):
        self.data_set = DomainUrl.objects.all()
    
    def validate_result(self, result):
        if not isinstance(result, str):
            return False
        if re.search(r'^Y$|^N$', result.upper()) is None:
            return False
        return True
    
    def inform(self, model):
        print(model.url)
    
    def reinform(self):
        print('Please answer Y or N')
    
    def result_callback(self, result, model):
        if result.upper() == 'Y':
            model.is_notice = True
        else:
            model.is_notice = False
        model.save()
