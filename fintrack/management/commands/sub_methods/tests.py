from exchange.models import Exchange


def exchange_close_utc():
    exchanges = Exchange.objects.all()
    for exchange in exchanges:
        print('{} {}'.format(exchange.symbol, exchange.get_market_close_utc()))
        exchange.get_market_close_utc()


def show_open_markets():
    for exchange in Exchange.objects.all():
        print('{} {}'.format(exchange.symbol, exchange.market_open()))
        if exchange.market_open():
            print('{} is open'.format(exchange.symbol))
