from common.models import DomainMst
from .navigation_book import NavigationBook
from bs4 import BeautifulSoup
from common.utils import (
    extract_domain_from_url_without_protocol as ext_domain, 
    extract_url_without_protocol as ext_url,
    convert_relative_path_to_absolute_path as conv_re_ab,
)
import requests

class Navigator:
    
    _initialized = False
    
    navigator_book = NavigationBook()
    
    banned_domain = ['www.instagram.com', 'www.facebook.com', 'www.youtube.com', 'twitter.com']
    
    def __init__(self):
        if not self._initialized:
            for model in DomainMst.objects.all():
                self.navigator_book.add_item(domain=model.domain, url=model.domain)
        self._initialized = True
        self.current_path = ''
    
    def get_next(self):
        url_page = self.navigator_book.get_item()
        return (url_page.item, url_page.method, url_page.params)
    
    def is_over(self):
        return self.navigator_book.all_checked
    
    def validate_reponse(self, response):
        if not isinstance(response, requests.models.Response):
            raise TypeError('responses has to be requests.models.Response')
    
    def add_navigaion_book(self, domain, url, method=None, params=None):
        if domain is None or url is None:
            return
        if domain in self.banned_domain:
            return
        
        kwargs = {
            'domain' : domain,
            'url'    : url
        }
        if method is not None:
            kwargs['method'] = method
        if params is not None:
            kwargs['params'] = params
        self.navigator_book.add_item(**kwargs)
        
    
    def navigate_by_html_tag(self, soup):
        self.navigate_by_a_tag(soup)
        self.navigate_by_form_tag(soup)
    
    def navigate_by_a_tag(self, soup):
        for link in soup.find_all('a', href=True):
            url = link['href']
            try:
                url = conv_re_ab(url, self.current_path)
                domain = ext_domain(url)
                url = ext_url(url)
            except Exception:
                domain = None
                url = None
            finally:
                self.add_navigaion_book(domain, url)
    
    def navigate_by_form_tag(self, soup):
        '''
        TODO navigate by form tag
        '''
        pass
    
    def analyze_response(self, response):
        self.validate_reponse(response)
        self.current_path = response.url
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navigate_by_html_tag(soup)
        pass
