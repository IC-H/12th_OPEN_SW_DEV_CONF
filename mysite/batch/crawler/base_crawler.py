import requests
import re
from django.core.validators import URLValidator


class BaseCrawler:
    
    valid_protocol = ['http', 'https']
    valid_encoindg = [
        'UTF-8',
        # English
        'ISO-8859-1', 'ISO-8859-2', 'ISO-8859-3', 'ISO-8859-4','ISO-8859-5', 'ISO-8859-6', 'ISO-8859-7', 'ISO-8859-8', 'ISO-8859-9', 'ISO-8859-10',
        # Korean
        'EUC-KR', 'ISO-2022-KR',
        # Japanese
        'EUC-JP', 'SHIFT_JIS', 'ISO-2022-JP',
    ]
    timeout = 10
    
    def __init__(self, protocol='https'):
        if not protocol in self.valid_protocol:
            raise ValueError('protocol has to be http or https')
        self.protocol = protocol
    
    def run(self):
        pass
    
    def set_encoding(self, response, to_encoding):
        if not isinstance(response, requests.models.Response):
            raise TypeError('request has to be instance of Response Class')
        if not isinstance(to_encoding, str):
            raise TypeError('to_encoding is has to be string')
        if not to_encoding.uper() in self.valid_encoindg:
            raise ValueError(
                'to_encoding can be \n' +
                ','.join(self.valid_encoindg) + '\n' +
                'Pleas check to_encoding you use'
            )
        
        if response.encoding.uper() != to_encoding.uper():
            response.encoding = to_encoding.uper()
    
    def validate_url(self, url):
        if not isinstance(url, str):
            raise TypeError('url has to be string')
        
        if not re.match("(^http|^https):\/\/", url):
            url = self.protocol + '://' + url
        valitator = URLValidator()
        valitator(url)
        return url
    
    def get_request(self, url):
        valid_url = self.validate_url(url)
        response = requests.get(valid_url, timeout=self.timeout)
        return response
    
    def validate_post_parameters(self, params):
        if not isinstance(params, dict):
            raise TypeError('data has to be dict')
    
    def post_request(self, url, params):
        self.validate_post_parameters(params)
        valid_url = self.validate_url(url)
        response = requests.post(valid_url, params, timeout=self.timeout)
        return response
