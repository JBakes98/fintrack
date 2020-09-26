from django.core.management import BaseCommand
from django.db.backends.utils import logger
from stock.utils import check_valid_tickers
from stock.services import StockMachineLearningService


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('Running test')
        tickers = ['AAL', 'AAPL', 'ACLS', 'ACGL', 'ACIW']
        cl_tickers = check_valid_tickers.check_valid_ticker(tickers)
        ml = StockMachineLearningService(stocks=cl_tickers)
        print(ml.get_stocks_correlation())
