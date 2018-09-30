from django.conf import settings

class BaseClassifier():
    """Base model of classfting the notice url"""
    def __init__(self):
    	self._did_learn = False
        self.load()

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

    def _preprocess(self): ## 전처리기능
        pass

    def teach(self): ## 학습
        pass

    def save_result(self):
        pass