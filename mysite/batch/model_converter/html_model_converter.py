from common.models import DomainUrl, Tag, LangMst, Word, HtmlVector
from batch.model_converter import BaseModelConverter
from bs4 import BeautifulSoup
from bs4.element import Tag as BsTag
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import requests

class HtmlVectorModelConverter(BaseModelConverter):
    
    banned_tag_list = ['style', 'script']
    
    class Meta:
        vector_model = HtmlVector
    
    def initialize(self):
        super().initialize()
        self._tag_log = {} # For check tag's duplication
    
    def is_tag_appendable(self, tag):
        if not isinstance(tag, BsTag):
            return False
        if tag.name in self.banned_tag_list:
            return False
        if tag.string is None:
            return False
        
        return True
    
    def _append_model(self, tag):
        log_of_current_tag = self._tag_log.get(tag.name, {'count' : 0})
        log_of_current_tag['count'] += 1
        self._tag_log[tag.name] = log_of_current_tag
        word_list = tag.string.split()
        for index, word in enumerate(word_list):
            try:
                language = detect(word)
            except LangDetectException:
                language = 'en'
            model = self.vector_model(
                url         = self.domain_url_model,
                tag         = Tag.find_by_tag_with_out_fail(tag.name),
                tag_order   = log_of_current_tag['count'],
                lang        = LangMst.find_by_language_with_out_fail(language),
                word        = Word.find_by_word_with_out_fail(word),
                word_order  = index + 1
            )
            self.append_vector_model_set(model)
    
    def _recursive_disassemble(self, page_element):
        if hasattr(page_element, 'contents'):
            for child in page_element.contents:
                self._recursive_disassemble(child)
        else:
            tag = page_element.find_parent()
            if self.is_tag_appendable(tag):
                self._append_model(tag)
    
    def convert(self, response):
        soup = BeautifulSoup(markup=response.content, features='html.parser')
        self._recursive_disassemble(soup)
    
    def revert(self):
        set = self.vector_model.objects.filter(url__exact=self.domain_url_model).order_by('tag', 'tag_order', 'word', 'word_order').select_related()
        pre_tag = None
        pre_tag_order = None
        row = None
        for model in set:
            if pre_tag == model.tag.tag and pre_tag_order == model.tag_order:
                row += ' ' + model.word.word
            else:
                if pre_tag is not None and pre_tag_order is not None:
                    print(row + '</' + pre_tag + '>')
                row = '<' + model.tag.tag + '>' + model.word.word
                pre_tag = model.tag.tag
                pre_tag_order = model.tag_order
