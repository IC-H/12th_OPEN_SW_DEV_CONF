from django.core.management.base import BaseCommand, CommandError
from batch.mail import YummyMailer

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        try:
            mailer = YummyMailer()
            mailer.send()
        except CommandError as e:
            print(e)