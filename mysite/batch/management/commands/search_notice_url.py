from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError
from batch.crawler import NoticeUrlCrawler

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('thread_num', nargs='?', type=int, default=10)
    
    def handle(self, *args, **options):
        try:
            for thread in range(options['thread_num']):
                crawler = NoticeUrlCrawler()
                crawler.start()
        except CommandError as e:
            print(e)
        except ValidationError as e:
            print(e)
        except (IntegrityError, DatabaseError) as e:
            print(e)
