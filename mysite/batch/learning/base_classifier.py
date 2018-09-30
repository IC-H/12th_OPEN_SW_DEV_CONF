from django.conf import settings
from django.core.exceptions import ValidationError

class BaseClassifier():
    """Base model of classfting the notice url"""
    def __init__(self):
        self._did_learn = False
        self.load()
    
    def __call__(self, *arg, **kwarg):
        if not self.did_learn:
            raise ValidationError('before classify you have to learn the classifier')
        self.classify(*arg, **kwarg)
    
    def load(self): # 학슴결과 불러오기
        pass
    
    ## 학습여부확인
    @property
    def did_learn(self):
        return self._did_learn
    
    @did_learn.setter
    def did_learn(self, flg):
        if not isinstance(flg, bool):
            raise TypeError('flg has to be bool')
        self._did_learn = flg
    
    def _preprocess(self, data): ## 전처리기능
        pass
    
    def teach(self, data): ## 학습
        pass
    
    def save_result(self):
        pass
    
    def classify(self, data):
        pass
