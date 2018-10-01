import urllib.request
from bs4 import BeautifulSoup
from common.models import DomainUrl, Tag


def Crawling(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    soup = BeautifulSoup(response, 'html.parser')
    return soup


def count_depth(tag):
    parent_tag = []
    while(tag.parent != None):
        tag = tag.parent
        parent_tag.append(tag.name)
    return len(parent_tag)


def get_tag_id(tag):
    try:
        tag_id = Tag.objects.filter(tag = tag).get().id
    except:
        new_tag = Tag(tag = tag)
        new_tag.save()
        tag_id = Tag.objects.filter(tag = tag).get().id
    return tag_id


def vectorize_by_depth(soup, url):
    vector = []
    url_id = DomainUrl.objects.filter(url = url).get().id
    for _tag in soup.find_all():
        tag_id = get_tag_id(_tag.name)
        vector.append([url_id, tag_id, count_depth(_tag)])
    return vector
