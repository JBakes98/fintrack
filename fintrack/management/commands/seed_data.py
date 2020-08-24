from django.core.management import BaseCommand
from fintrack.management.commands.sub_methods import countries, exchanges, fix_empty_sector_industry, index
from fintrack_be.models import Sector, Industry, Company


# python manage.py seed
class Command(BaseCommand):
    help = 'Seed the database for development'

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help='Mode')

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])


def run_seed(self, mode):
    # countries.create_countries()
    # exchanges.create_exchanges()

    # Create empty objects for instances that dont have parents
#    Sector.objects.create_sector(name='N/A')
 #   Industry.objects.create_industry(name='N/A', sector='N/A')
   # Company.objects.create_company(short_name='N/A',
   #                                 long_name='Non Parented Holding Company',
   #                                 summary='Company for holding Stock instances that dont have a known parent Company',
   #                                 industry=Industry.objects.get(name='N/A'))

    # Create all exchange stocks
    exchanges.add_nasdaq_stocks()
    exchanges.add_nyse_stocks()
    exchanges.add_lse_stocks()

    # Run fix to remove empty sector and industry created during seeding
    fix_empty_sector_industry.fix()
    exchanges.seed_exchange_stocks_data()

    # Create Indices and add constituents
    index.create_indices()
    index.create_constituents()
