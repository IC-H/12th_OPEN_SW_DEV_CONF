from django.core.exceptions import FieldError, ValidationError
from .item import CheckableItem
from encodings.punycode import insertion_sort
from builtins import str

class MetaContainer(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        parents = [b for b in bases if isinstance(b, MetaContainer)]
        if not parents:
            return super().__new__(cls, name, bases, attrs, **kwargs)
        
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)
        meta = attrs.pop('Meta', None) or getattr(new_class, 'Meta', None)
        '''
        Set a container model to class
        '''
        if meta is None:
            raise FieldError('Container class has to have class attribue called "Meta"')
        if not hasattr(meta, 'item_model'):
            raise FieldError('Meta attributes has to have "item_model"')
        item_model = getattr(meta, 'item_model')
        if not issubclass(item_model, CheckableItem):
            raise TypeError('"item_model" has to be class of "CheckableItem"')
        setattr(new_class, 'item_model', item_model)
        item_label = 'item'
        if hasattr(meta, 'item_label'):
            item_label = getattr(meta, 'item_label')
            if not isinstance(item_label, str):
                raise TypeError('item_label has to be string')
        setattr(new_class, 'item_label', item_label)
        return new_class

class BaseContainer(CheckableItem, metaclass=MetaContainer):
    def __init__(self, label='label', **kwargs):
        self.label = label
        super().__init__([])
    
    def _check_all_checked(self):
        flg = True
        for content in self.item:
            if not content.is_checked:
                flg = False
                break
        self.is_checked = flg
    
    @property
    def all_checked(self):
        return self.is_checked
    
    def is_same(self, label):
        return self.label == label
    
    def _get_key_words(self, *args, **kwargs):
        key_word = kwargs.pop(self.item_label, None)
        if key_word is None:
            key_word = args[0] if len(args) > 0 else None
            args = (args[index + 1] for index in range(len(args)-1)) if len(args) > 1 else ()
        return (key_word, args, kwargs)
    
    def search_item(self, *args, **kwargs):
        item, args, kwargs = self._get_key_words(*args, **kwargs)
        for content in self.item:
            if content.is_same(item):
                return content
        return None
    
    def search_not_checked_item(self):
        for content in self.item:
            if not content.is_checked:
                return content
        return None
    
    def add_item(self, *args, **kwargs):
        item, args, kwargs = self._get_key_words(*args, **kwargs)
        content = self.search_item(item)
        if content is None:
            self.item.append(self.item_model(item, *args, **kwargs))
            content = self.search_item(item)
            self.is_checked = False
        if isinstance(content, BaseContainer):
            content.add_item(*args, **kwargs)
    
    def get_item(self):
        content = self.search_not_checked_item()
        if content is None:
            return None
        item = content.get_item()
        self._check_all_checked()
        return item
