from common.models import Tag, LangMst, Word, HtmlVectorWithDepth
from batch.model_converter import HtmlVectorModelConverter
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

class HtmlVectorWithDepthModelConverter(HtmlVectorModelConverter):
    
    class Meta:
        vector_model = HtmlVectorWithDepth
    
    def count_depth(self, tag):
        parent_tag = []
        while(tag.parent != None):
            tag = tag.parent
            parent_tag.append(tag.name)
        return len(parent_tag) + 1

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
                word_order  = index + 1,
                depth       = self.count_depth(tag)
            )
            self.append_vector_model_set(model)
