from django.db import models, transaction, DatabaseError, IntegrityError
from common.models import LangMst
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

class Word(models.Model):
    word = models.CharField(unique=True, max_length=45)
    lang = models.ForeignKey(LangMst, on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'word'
    
    @staticmethod
    @transaction.atomic
    def find_by_word_with_out_fail(word):
        try:
            model = Word.objects.filter(word__exact=word).get()
        except Word.DoesNotExist:
            try:
                with transaction.atomic():
                    try:
                        language = detect(word)
                    except LangDetectException:
                        language= 'en'
                    language_model = LangMst.find_by_language_with_out_fail(language)
                    model = Word(word=word, lang=language_model)
                    model.save()
            except (DatabaseError, IntegrityError):
                # For parallel thread
                # If word is registerd with another process search one more time
                model = Word.objects.filter(word__exact=word).get()
        return model
