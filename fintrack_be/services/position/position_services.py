from fintrack_be.models import Stock, Position
import datetime


class PositionMessenger:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


class PositionService(object):
    @staticmethod
    def open_position(user, data):
        if 'open_price' not in data:
            instrument = Stock.objects.get(ticker=data['instrument'])
            open_price = instrument.latest_price
        else:
            open_price = data['open_price']

        if 'open_date' not in data:
            open_date = datetime.datetime.now()
        else:
            open_date = data['open_date']

        cost = open_price * data['quantity']
        user.update_funds(cost)
        position = Position.objects.create(user=user, open_price=open_price, open_date=open_date, **data)

        return position

    @staticmethod
    def _prepare_payload():
        return None