import re

def extract_domain_from_url_without_protocol(url):
    '''
    https://project.oss.kr/index.do -> project.oss.kr
    '''
    return re.search(r"((?<=(^http:\/\/))|(?<=^https:\/\/))[^\/]*", url).group()

def extract_url_without_protocol(url):
    '''
    https://project.oss.kr/index.do -> project.oss.kr/index.do
    '''
    return re.search(r"((?<=(^http:\/\/))|(?<=^https:\/\/)).*", url).group()

def convert_relative_path_to_absolute_path(url, current_path):
    '''
    "url" : /example.php
    "current_path" : https://project.oss.kr/index.do
    -> https://project.oss.kr/index.do/example.php
    '''
    removing_slash = re.search(r'^\/', url)
    if removing_slash is None:
        return url
    return current_path + removing_slash.group()

def extract_url_without_get_params(url):
    '''
    https://project.oss.kr/index.do?index=111 -> https://project.oss.kr/index.do
    '''
    return re.search(r'^[^?]*', url).group()

def extract_url_without_last_slash(url):
    '''
    https://project.oss.kr/index.do// -> https://project.oss.kr/index.do
    '''
    return re.search(r'^(.+?)[/]*$', url).group(1)

def looks_like_notice_url(url):
    return re.search(r'notice|list', url) is not None

__all__ = [
    'extract_domain_from_url_without_protocol', 'extract_url_without_protocol', 'convert_relative_path_to_absolute_path',
    'extract_url_without_get_params', 'extract_url_without_last_slash', 'looks_like_notice_url'
]
