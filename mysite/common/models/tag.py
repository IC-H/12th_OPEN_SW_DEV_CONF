from django.db import models, transaction, DatabaseError, IntegrityError

class Tag(models.Model):
    # tag is constructed with lower alphabet
    tag = models.CharField(unique=True, max_length=45)
    
    class Meta:
        managed = False
        db_table = 'tag'
    
    def save(self, force_insert=False, force_update=False, using=None, 
        update_fields=None):
        self.tag = self.tag.lower()
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
    
    @staticmethod
    @transaction.atomic
    def find_by_tag_with_out_fail(tag):
        try:
            model = Tag.objects.filter(tag__exact=tag).get()
        except Tag.DoesNotExist:
            try:
                with transaction.atomic():
                    model = Tag(tag=tag)
                    model.save()
            except (DatabaseError, IntegrityError):
                # For parallel thread
                # If tag is registerd with another process search one more time
                model = Tag.objects.filter(domain__exact=domain).get()
        return model
