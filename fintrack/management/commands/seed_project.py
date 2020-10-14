from django.core import management
from django.core.management import BaseCommand
from django.db.backends.utils import logger


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('Seeding Project Data...')
        management.call_command('seed_countries')
        logger.info('Seeded Country data.')

        management.call_command('seed_exchanges')
        management.call_command('seed_exchange_stocks')
        logger.info('Seeded Exchanges and Stock data')

        management.call_command('fix_empty_industry')
        management.call_command('fix_empty_sector')

        logger.info('Seeded Fintrack data.')

