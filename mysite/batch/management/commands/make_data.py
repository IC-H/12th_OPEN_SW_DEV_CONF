from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError
from batch.learning import NoticeUrlDataMaker

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        try:
            maker = NoticeUrlDataMaker()
            maker()
        except CommandError as e:
            print(e)
