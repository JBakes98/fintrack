from django.core.management import BaseCommand
from django.db.backends.utils import logger

from country.utils import seed_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        """ Creates the countries """
        logger.info('Creating Countries...')
        seed_data.seed_countries()
        logger.info('Added Countries')


