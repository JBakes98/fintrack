from django.db.backends.utils import logger
from country import country_data


def create_countries():
    """ Creates the countries """
    logger.info('Creating Countries...')
    country_data.create_country_instances()
    logger.info('Added Countries')

