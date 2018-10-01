from django.db import models, transaction, DatabaseError, IntegrityError

class LangMst(models.Model):
    # language is constructed with lower alphabet
    language = models.CharField(unique=True, max_length=45)
    
    class Meta:
        managed = False
        db_table = 'lang_mst'
    
    def save(self, force_insert=False, force_update=False, using=None, 
        update_fields=None):
        self.language = self.language.lower()
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
    
    @staticmethod
    @transaction.atomic
    def find_by_language_with_out_fail(language):
        try:
            model = LangMst.objects.filter(language__exact=language).get()
        except LangMst.DoesNotExist:
            try:
                with transaction.atomic():
                    model = LangMst(language=language)
                    model.save()
            except (DatabaseError, IntegrityError):
                # For parallel thread
                # If language is registerd with another process search one more time
                model = LangMst.objects.filter(language__exact=language).get()
        return model
