from dataclasses import dataclass

from django.db import IntegrityError
from django.db.models import Q

from company.models import Company
from exchange.models import Exchange
from stock.models import Stock


@dataclass
class StockDto:
    ticker: str
    name: str
    company: str


class StockService:
    def create(self, ticker, name, exchange):
        try:
            exchange = Exchange.objects.get(Q(symbol=exchange) | Q(name=exchange))
            company = get_stock_company(ticker)
            Stock.objects.update_or_create(ticker=ticker,
                                           name=name,
                                           exchange=exchange,
                                           company=company)
            print('{} created'.format(ticker))

        except Exchange.DoesNotExist as e:
            print('{}: {}'.format(exchange, e))
        except Company.DoesNotExist as e:
            print('{}'.format(e))
        except KeyError as e:
            print('{}'.format(e))
        except IntegrityError as e:
            print(e)

    def get_company(self, ticker):
        """
            Method for getting the parent company of the specified stock, if company cannot be found
            then it will call the create_company method to create the company. If the method fails
            it will attempt 3 times before failing completely.
            :param ticker: Stock ticker
            :return: Stocks parent Company
            """
        # Returns JSON data that contains data on the stock
        stock = yf.Ticker(ticker)
        attempts = 3

        for i in range(attempts):
            try:
                json = stock.info
                # Get company names from the JSON response data
                short_company_name, long_company_name = extract_company_names_from_json(json)

                try:
                    return get_company(short_company_name, long_company_name)
                except Company.DoesNotExist:
                    create_company_json(json)
                    return get_company(short_company_name, long_company_name)

            except ValueError:
                print('{} cannot find parent company'.format(ticker))
                return get_company('N/A', 'Non linked objects')
            except KeyError:
                return get_company('N/A', 'Non linked objects')
            except IncompleteRead as e:
                print(e)
            except MultipleObjectsReturned as e:
                print(e)
            # except HTTPError as e:
            #     if i < attempts - 1:
            #         print(e)
            #         print('Retrying attempt {}'.format(i))
            #         continue
            #     else:
            #         print(e)
            #         print('Attempted {} times, all unsuccessful'.format(attempts))
            #     break
