from django.core.management.base import BaseCommand, CommandError
from batch.crawler import NoticeCrawlerLite

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        try:
            crawler = NoticeCrawlerLite()
            crawler.run()
        except CommandError as e:
            print(e)