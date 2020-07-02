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
            data['open_price'] = instrument.latest_price

        if 'open_date' not in data:
            data['open_date'] = datetime.datetime.now()

        cost = data['open_price'] * data['quantity']
        user.update_funds(cost)

        position = Position.objects.create(user=user, **data)
        return position.__dict__

    @staticmethod
    def _prepare_payload():
        return None