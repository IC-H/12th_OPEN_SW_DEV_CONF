from django.core.exceptions import ValidationError, FieldError
from numpy.lib.function_base import iterable

class MeataDataMaker(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [b for b in bases if isinstance(b, MeataDataMaker)]
        if not parents:
            return super().__new__(cls, name, bases, attrs, **kwargs)
        
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)
        '''
        Set question which be used for data maker
        '''
        meta = attrs.pop('Meta', None) or getattr(new_class, 'Meta', None)
        if meta is None:
            raise FieldError('DataMaker class has to have class attribue claaed "Meta"')
        if not hasattr(meta, 'question'):
            raise FieldError('Meta attributes has to have "question"')
        if not isinstance(meta.question, str):
            raise TypeError('question has to be string')
        
        setattr(new_class, 'question', meta.question)
        return new_class

class BaseDataMaker(metaclass=MeataDataMaker):
    """
    Base Class of Data Maker
    Data Maker make user easy to make data
    'qustion' in Meata class is question for make data
    before calling this class, setting data_set is essential
    """
    def __init__(self):
        self._data_set = None
    
    @property
    def data_set(self):
        return self._data_set
    
    @data_set.setter
    def data_set(self, data_set):
        self._data_set = data_set
    
    def inform(self, model):
        """
        inform to user for make data
        """
        pass
    
    def re_inform(self, model):
        """
        reinform to user when input is not validate
        """
        pass
    
    def validate_result(self, result):
        return True
    
    def result_callback(self, result, model):
        pass
    
    def question_to_teacher(self, model):
        self.inform(model)
        result = input(self.question)
        if not self.validate_result(result):
            self.re_inform(model)
            self.question_to_teacher(model)
        else:
            self.result_callback(result, model)
    
    def gather_data_set(self):
        pass
    
    def validate_data_set(self):
        if self.data_set is None:
            raise ValidationError('Before calling, you have to set the data set')
        if not iterable(self.data_set):
            raise ValidationError('Before calling, you have to set the data set')
    
    def __call__(self):
        self.gather_data_set()
        self.validate_data_set()
        for model in self.data_set:
            self.question_to_teacher(model)
