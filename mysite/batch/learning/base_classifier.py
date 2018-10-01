from django.conf import settings
from django.core.exceptions import ValidationError
from sklearn.externals import joblib

class MeataClassiifer(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [b for b in bases if isinstance(b, MeataClassiifer)]
        if not parents:
            return super().__new__(cls, name, bases, attrs, **kwargs)
        
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)
        '''
        Set model which be used for vectorize
        '''
        meta = attrs.pop('Meta', None) or getattr(new_class, 'Meta', None)
        if meta is None:
            raise FieldError('Vectorize class has to have class attribue claaed "Meta"')
        if not hasattr(meta, 'result_file_name'):
            raise FieldError('Meta attributes has to have "result_file_name"')
        if not isinstance(meta.result_file_name, str):
            raise TypeError('result_file_name has to be string')
        
        setattr(new_class, 'result_file_name', meta.result_file_name)
        return new_class


class BaseClassifier(metaclass=MeataClassiifer):
    """Base model of classfting the notice url"""
    def __init__(self):
        self._did_learn = False
        self.load()
    
    def __call__(self, *arg, **kwarg):
        if not self.did_learn:
            raise ValidationError('before classify you have to learn the classifier')
        return self.classify(*arg, **kwarg)
    
    def set_model(self):
        pass
    
    def load(self): # 학슴결과 불러오기
        try:
            self.model = joblib.load(settings.BASE_DIR + '/batch/learning/' + self.result_file_name)
            self.did_learn = True
        except Exception:
            self.model = None
            self.set_model()
            self.did_learn = False
    
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
        if not self.did_learn:
            raise ValidationError('before save result you have to learn the classifier')
        joblib.dump(self.model, settings.BASE_DIR + '/batch/learning/' + self.result_file_name)
    
    def classify(self, data):
        pass
