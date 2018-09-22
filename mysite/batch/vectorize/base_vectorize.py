from django.core.exceptions import FieldError, ValidationError
from django.db.models import Model, QuerySet
from builtins import str

class MeataVectorize(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [b for b in bases if isinstance(b, MeataVectorize)]
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

class BaseVectorize(metaclass=MeataVectorize):
    '''
    Convert Model or QuerySet of Model to list of vector
    '''
    def __init__(self, indices):
        '''
        indices is list of index which is column of the vector_model
        '''
        if not isinstance(indices, list):
            raise TypeError('indices has to be list')
        if len(indices) < 1:
            raise ValidationError('indices has to have more than one element')
        for index in indices:
            if not isinstance(index, str):
                raise ValidationError('elements of indices has to be string')
            if not hasattr(self.vector_model, index):
                raise ValidationError('elements of indices has to be column of vector_model')
        
        self._vector_set = []
        self.indices     = indices
    
    def _append_vector_set(self, model):
        vector = []
        for index in self.indices:
            vector.append(getattr(model, index))
        self._vector_set.append(vector)
    
    def vectorize(self, model=None, query_set=None):
        if model is not None:
            self.validate_model(model)
            self._append_vector_set(model)
        if query_set is not None:
            self.validate_query_set(query_set)
            for model in query_set:
                self._append_vector_set(model)
    
    def validate_model(self, model):
        if not isinstance(model, self.vector_model):
            raise ValidationError('model has to be instance of vector_model')
        for index in self.indices:
            if not getattr(model, index, False):
                raise ValidationError('model has to set %s attribute' % index)
    
    def validate_query_set(self, query_set):
        if not isinstance(query_set, QuerySet):
            raise ValidationError('query_set has to be instance of QuerySet')
        for model in query_set:
            self.validate_model(model)
    
    def get_vector_set(self):
        return self._vector_set
