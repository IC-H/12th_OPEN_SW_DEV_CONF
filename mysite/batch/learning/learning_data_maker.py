from common.models import DomainUrl
import re

class DataMaker:
    
    def question_to_teacher(self, model):
        print('https://' + model.url)
        result = input('Is url for notice ? Y or N  :  ')
        if not isinstance(result, str):
            print('Please answer Just Y or N')
            self.question_to_teacher(model)
        elif re.search(r'^Y$|^N$', result.upper()) is None:
            print('Please answer Just Y or N')
            self.question_to_teacher(model)
        if result.upper() == 'Y':
            model.is_notice = True
        else:
            model.is_notice = False
        model.save()
    
    def __call__(self):
        for model in DomainUrl.objects.all():
            self.question_to_teacher(model)
