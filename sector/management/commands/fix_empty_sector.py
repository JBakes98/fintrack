from django.core.management import BaseCommand
from django.db.backends.utils import logger

from sector.models import Sector


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('Correcting Sector data...')
        sector = Sector.objects.get(pk=7)
        sector.delete()
        logger.info('Finished changes.')
