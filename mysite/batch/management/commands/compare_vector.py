from django.core.management.base import BaseCommand, CommandError
from batch.crawler import NoticeCrawler

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        try:
            crawler = NoticeCrawler()7t6f