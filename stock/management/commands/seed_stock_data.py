from django.core.management import BaseCommand
from django.db.backends.utils import logger
from stock.models import Stock
from stock.services import StockDataService
from stock.utils import df_util


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('Seeding Stock price data...')
        for stock in Stock.objects.all():
            logger.info('Seeding {}...'.format(stock.ticker))
            service = StockDataService(ticker=stock.ticker, name=stock.name, exchange=stock.exchange)
            df_util.bulk_stock_price_data_to_model(service.get_stock_data())
            logger.info('Finished seeding {}...'.format(stock.ticker))
        logger.info('Finished seeding stock data.')
