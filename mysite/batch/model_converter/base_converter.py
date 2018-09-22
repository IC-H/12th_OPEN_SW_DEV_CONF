from django.core.exceptions import FieldError, ValidationError
from django.db.models import Model, QuerySet
from django.db import transaction, DatabaseError, IntegrityError
from bs4 import BeautifulSoup

class MetaConverter(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [b for b in bases if isinstance(b, MetaConverter)]
        if not parents:
            return super().__new__(cls, name, bases, attrs, **kwargs)
        
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)
        '''
        Set model which be used for vectorize
        '''
        meta = attrs.pop('Meta', None) or getattr(new_class, 'Meta', None)
        if meta is None:
            raise FieldError('Vectorize class has to have class attribue claaed "Meta"')
        if not hasattr(meta, 'vector_model'):
            raise FieldError('Meta attributes has to have "vector_model"')
        if not issubclass(meta.vector_model, Model):
            raise TypeError('vector_model has to be Model class produced by django')
        
        setattr(new_class, 'vector_model', meta.vector_model)
        return new_class

class BaseModelConverter(metaclass=MetaConverter):
    '''
    convert instance of BeautifulSoup to set of vector_model
    '''
    def __init__(self):
        self.initialize()
    
    def initialize(self):
        self.html = None
        self._vector_model_set = []
    
    def validate_soup(self, soup):
        if not isinstance(soup, BeautifulSoup):
            raise TypeError('soup has to be instance of BeautifulSoup')
    
    def validate_vector_model(self, model):
        if not isinstance(model, self.vector_model):
            raise TypeError('model has to be instance of vector_model')
    
    def run(self, soup):
        self.validate_soup(soup)
        self.convert(soup)
    
    def append_vector_model_set(self, model):
        self.validate_vector_model(model)
        self._vector_model_set.append(model)
    
    def convert(self, soup):
        pass
    
    def get_vector_model_set(self):
        return self._vector_model_set
    
    @transaction.atomic
    def save_model_set(self):
        with transaction.atomic():
            for model in self.get_vector_model_set():
                model.save()
