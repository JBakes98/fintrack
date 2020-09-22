from django.core.management import BaseCommand
from exchange.utils import seed_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        seed_data.create_all_exchange_stocks()

