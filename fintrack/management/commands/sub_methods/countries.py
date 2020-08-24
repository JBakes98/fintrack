from django.db.backends.utils import logger
from fintrack_be.utils.seed_util import seed_countries


def create_countries():
    """ Creates the countries """
    logger.info('Creating Countries...')
    seed_countries()
    logger.info('Added Countries')

