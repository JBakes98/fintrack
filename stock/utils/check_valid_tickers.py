from stock.models import Stock


def check_valid_ticker(tickers: []):
    """
    This method takes a list of tickers and checks that they
    are valid tickers for stocks stored in the DB, if they are
    valid then theyre appended to the valid list which is returned.
    :param tickers: List of tickers
    :return: List of valid stock tickers
    """

    valid_tickers = []
    for ticker in tickers:
        try:
            stock = Stock.objects.get(ticker=ticker)
            valid_tickers.append(stock.ticker)
        except Stock.DoesNotExist:
            pass

    return valid_tickers
