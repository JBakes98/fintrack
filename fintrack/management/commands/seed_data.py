from django.core.management import BaseCommand
from fintrack.management.commands.sub_methods import countries, exchanges, fix_empty_sector_industry, index
from sector import sector_data
from fintrack_be.functions.industry import industry_data
from fintrack_be.functions.company import company_data


# python manage.py seed
class Command(BaseCommand):
    help = 'Seed the database for development'

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help='Mode')

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])


def run_seed(self, mode):
    countries.create_countries()
    exchanges.create_exchanges()

    # Create empty objects for instances that dont have parents
    sector_data.create_sector('N/A')
    industry_data.create_industry('N/A', 'N/A')
    company_data.create_company('N/A',
                                'Non Parented Holding Company',
                                'Company for holding Stock instances that dont have a known parent Company',
                                'N/A')

    exchanges.create_all_exchange_stocks()
    # Run fix to remove empty sector and industry created during seeding
    fix_empty_sector_industry.fix()
    exchanges.seed_exchange_stocks_data()

    index.create_indices()
    index.create_constituents()