# records/management/commands/train_model.py

from django.core.management.base import BaseCommand
from records.train_model import train

class Command(BaseCommand):
    help = 'Train the stock prediction model using historical data.'

    def handle(self, *args, **kwargs):
        train()
        self.stdout.write(self.style.SUCCESS('Model training completed.'))
