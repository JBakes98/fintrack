from django.core.management import BaseCommand
from django.db.backends.utils import logger
from stock.utils import valid_tickers
from stock.services import StockMachineLearningService
import yfinance


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('Running test')
        stock = yfinance.Ticker('AAPL')
        print('Info: {}'.format(stock.info))
        print('Calendar: {}'.format(stock.calendar))
        print('Recommendations: {}'.format(stock.recommendations))
        print('Actions {}'.format(stock.actions))
        print('Sustainability: {}'.format(stock.sustainability))
