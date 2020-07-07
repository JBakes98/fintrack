from fintrack_be.exceptions import PositionNotOpenError
from fintrack_be.models import Stock, Position, User
import datetime


class PositionService:
    def open_position(self, user, data):
        data = self._prepare_open_payload(data)
        user.update_funds(data['cost'])
        Position.objects.create(user=user, **data)

    def close_position(self, position_id, data):
        position = Position.objects.get(pk=position_id)
        if not position.is_open:
            raise PositionNotOpenError

        data = self._prepare_close_payload(data, position)

        position.result = data['result']
        position.close_date = data['close_date']
        position.close_price = data['close_price']
        position.save()

        user = position.user
        user.update_funds(position.result)
        user.update_result(position.result)

    @staticmethod
    def _prepare_open_payload(data):
        if 'open_price' not in data:
            instrument = Stock.objects.get(ticker=data['instrument'])
            data['open_price'] = instrument.latest_price
        if 'open_date' not in data:
            data['open_date'] = datetime.datetime.now()
        data['cost'] = data['open_price'] * data['quantity']

        return data

    @staticmethod
    def _prepare_close_payload(data, position):
        if 'close_price' not in data:
            instrument = position.instrument
            data['close_price'] = instrument.latest_price
        if 'close_date' not in data:
            data['close_date'] = datetime.datetime.now()
        data['result'] = (data['close_price'] - position.open_price) * position.quantity

        return data
