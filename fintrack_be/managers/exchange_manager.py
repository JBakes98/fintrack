from django.db import models


class ExchangeManager(models.Manager):
    use_in_migrations = True

    def _create_exchange(self, symbol, name, country, timezone, opening_time, closing_time):
        exchange = self.model(
            symbol=symbol,
            name=name,
            country=country,
            timezone=timezone,
            opening_time=opening_time,
            closing_time=closing_time
        )
        exchange.save(using=self._db)

        return exchange

    def create_exchange(self, symbol, name, country, timezone, opening_time, closing_time):
        return self._create_exchange(symbol, name, country, timezone, opening_time, closing_time)

    def with_stock_count(self):
        """
        Method to get all exchange objects and the number of stocks registered to the exchange
        """
        from django.db import connection
        from fintrack_be.models.country import Country
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT e.id, e.symbol, e.name, e.country_id, e.timezone, e.opening_time, e.closing_time, COUNT(*)
            FROM fintrack_be_exchange e, fintrack_be_stock s
            WHERE e.id = s.exchange_id
            GROUP BY e.id, e.symbol
            ORDER BY e.symbol DESC""")
            result_list = []

            for row in cursor.fetchall():
                e = self.model(id=row[0],
                               symbol=row[1],
                               name=row[2],
                               country=Country.objects.get(pk=row[3]),
                               timezone=row[4],
                               opening_time=row[5],
                               closing_time=row[6])
                e.num_stocks = row[7]
                result_list.append(e)

            return result_list
