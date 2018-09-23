from django.core.exceptions import FieldError, ValidationError
from django.db.models import Model, QuerySet
from django.db import transaction, DatabaseError, IntegrityError
from common.models import DomainMst, DomainUrl
import requests
import re

class MetaConverter(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [b for b in bases if isinstance(b, MetaConverter)]
        if not parents:
            return super().__new__(cls, name, bases, attrs, **kwargs)
        
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)
        '''
        Set model which be used for converter
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
    convert instance of requests.models.Response to set of vector_model
    '''
    def __init__(self):
        self.initialize()
    
    def initialize(self):
        self.html = None
        self._domain_url_model = None
        self._domain_mst_model = None
        self._vector_model_set = []
    
    def validate_response(self, response):
        if not isinstance(response, requests.models.Response):
            raise TypeError('soup has to be instance of requests.models.Response')
    
    def validate_vector_model(self, model):
        if not isinstance(model, self.vector_model):
            raise TypeError('model has to be instance of vector_model')
    
    @transaction.atomic
    def identify_url(self, response):
        '''
        Identiry response url
        If url's domain and url are already registed their table, read it.
        If not registed, regist them and read it.
        '''
        domain = re.search(r"((?<=(^http:\/\/))|(?<=^https:\/\/))[^\/]*", response.url).group()
        url = re.search(r"((?<=(^http:\/\/))|(?<=^https:\/\/)).*", response.url).group()
        self._domain_mst_model = DomainMst.find_by_domain_with_out_fail(domain)
        self._domain_url_model = DomainUrl.find_by_url_with_out_fail(url)
    
    @property
    def domain_url_model(self):
        return self._domain_url_model
    
    @property
    def domain_mst_model(self):
        return self._domain_mst_model
    
    def run(self, response):
        self.validate_response(response)
        self.identify_url(response)
        self.convert(response)
    
    def append_vector_model_set(self, model):
        self.validate_vector_model(model)
        self._vector_model_set.append(model)
    
    def convert(self, response):
        pass
    
    @property
    def vector_model_set(self):
        return self._vector_model_set
    
    @transaction.atomic
    def save_model_set(self):
        with transaction.atomic():
            for model in self.get_vector_model_set():
                model.save()
