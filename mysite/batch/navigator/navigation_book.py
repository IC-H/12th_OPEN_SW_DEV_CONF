from .item import CheckableItem
from .base_container import BaseContainer

class UrlPage(CheckableItem):
    def __init__(self, url, method='GET', params={}):
        super().__init__(url)
        self.method = method
        self.params = params

class DomainChapter(BaseContainer):
    
    class Meta:
        item_model = UrlPage
        item_label = 'url'
    
    def __init__(self, domain, **kwargs):
        super().__init__(domain, **kwargs)
    
    def add_item(self, url, *args, **kwargs):
        super().add_item(url=url, **kwargs)

class NavigationBook(BaseContainer):
    
    class Meta:
        item_model = DomainChapter
        item_label = 'domain'
    
    def add_item(self, domain, url, *args, **kwargs):
        super().add_item(domain=domain, url=url, *args, **kwargs)
