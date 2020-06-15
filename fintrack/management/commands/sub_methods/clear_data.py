from django.db.backends.utils import logger


def clear_data():
    """Deletes all table data"""
    logger.info('Delete all Object instances')

