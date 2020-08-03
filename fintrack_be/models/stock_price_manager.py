from django.db import models


class StockPriceManager(models.Manager):
    use_in_migrations = True

    def _create_price_data(self, timestamp, stock, high, low, open, close, volume, change, change_perc):
        price = self.model(
            timestamp=timestamp,
            stock=stock,
            high=high,
            low=low,
            open=open,
            close=close,
            volume=volume,
            change=change,
            change_perc=change_perc
        )
        price.save(using=self._db)

        return price

    def create_price_data(self, timestamp, stock, high, low, open, close, volume, change, change_perc):
        return self._create_price_data(timestamp, stock, high, low, open, close, volume, change, change_perc)

    def create_df_data(self, df):
        """
        Method that iterates of a stock price dataframe and creates its relevent models,
        this doesnt use bulk create and inserts data until it hits an already existing
        entry.
        :param df: Stock price dataframe
        """
        import decimal
        from django.db import IntegrityError

        for row in df[::-1].itertuples():
            try:
                self._create_price_data(timestamp=getattr(row, 'Index'),
                                        open=getattr(row, 'open'),
                                        high=getattr(row, 'high'),
                                        low=getattr(row, 'low'),
                                        close=getattr(row, 'close'),
                                        volume=getattr(row, 'volume'),
                                        stock=getattr(row, 'stock'),
                                        change=getattr(row, 'change'),
                                        change_perc=getattr(row, 'change_perc'))
            except IntegrityError as e:
                print('{}'.format(e))
                break
            except decimal.InvalidOperation as e:
                print(e)

    def create_bulk_data(self, df):
        """
        Same method as stock_price_data_df_to_model however iterates
        through the df but uses the bulk_create method to increase
        insert efficiency.
        :param df: Dataframe containing stock price data
        """
        import decimal
        from django.db import IntegrityError

        try:
            data = [self.model(timestamp=getattr(row, 'Index'),
                               open=getattr(row, 'open'),
                               high=getattr(row, 'high'),
                               low=getattr(row, 'low'),
                               close=getattr(row, 'close'),
                               volume=getattr(row, 'volume'),
                               stock=getattr(row, 'stock'),
                               change=getattr(row, 'change'),
                               change_perc=getattr(row, 'change_perc')
                               )
                    for row in df.itertuples()]
            self.model.objects.bulk_create(data)

        except IntegrityError as e:
            print('Already contain data for this stock {}'.format(e))
        except decimal.InvalidOperation as e:
            print(e)
