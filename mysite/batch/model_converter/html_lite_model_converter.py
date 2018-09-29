from common.models import DomainUrl, Tag, HtmlVectorLite
from batch.model_converter import BaseModelConverter
from bs4 import BeautifulSoup
from bs4.element import Tag as BsTag
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import requests

class HtmlVectorLiteModelConverter(BaseModelConverter):

    class Meta:
        vector_model = HtmlVectorLite
    
    def initialize(self):
        super().initialize()
        self._tag_log = {} # For check tag's duplication
    
    def is_tag_appendable(self, tag):
        if not isinstance(tag, BsTag):
            return False
        return True

    def count_depth(self, tag):
        parent_tag = []
        while(tag.parent != None):
            tag = tag.parent
            parent_tag.append(tag.name)
        return len(parent_tag)

    def _append_model(self, tag):
        log_of_current_tag = self._tag_log.get(tag.name, {'count' : 0})
        log_of_current_tag['count'] += 1
        self._tag_log[tag.name] = log_of_current_tag
        model = self.vector_model(
            url         = self.domain_url_model,
            tag         = Tag.find_by_tag_with_out_fail(tag.name),
            tag_order   = log_of_current_tag['count'],
            depth       = self.count_depth(tag)
        )
        self.append_vector_model_set(model)
    
    def _recursive_disassemble(self, page_element):
        if self.is_tag_appendable(page_element):
            self._append_model(page_element)
        if hasattr(page_element, 'contents'):
            for child in page_element.contents:
                self._recursive_disassemble(child)
    
    def convert(self, response):
        soup = BeautifulSoup(markup=response.content, features='html.parser')
        self._recursive_disassemble(soup)

    def revert(self):
        set = self.vector_model.objects.filter(url__exact=self.domain_url_model).order_by('id').select_related()
        pre_tag = None
        pre_tag_order = None
        row = None
        for model in set:
            if pre_tag is not None and pre_tag_order is not None:
                print(row + '</' + pre_tag + '>')
            row = '    '*model.depth + '<' + model.tag.tag + '>'
            pre_tag = model.tag.tag
            pre_tag_order = model.tag_order