from django.core.management import BaseCommand
from exchange.models import Exchange
from sector.models import Sector
from industry.models import Industry
from company.models import Company
from stock.models import Stock, StockPriceData
from index.models import Index, IndexConstituents


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help='Mode')

    def handle(self, *args, **options):
        self.stdout.write('Cleaning DB')
        clean_db(self, options['mode'])
        self.stdout.write('done')


def clean_db(self, mode):
    IndexConstituents.objects.all().delete()
    Index.objects.all().delete()
    StockPriceData.objects.all().delete()
    Stock.objects.all().delete()
    Company.objects.all().delete()
    Industry.objects.all().delete()
    Sector.objects.all().delete()
    Exchange.objects.all().delete()
