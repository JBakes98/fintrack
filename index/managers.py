from django.db import models


class IndexManager(models.Manager):
    use_in_migrations = True

    def _create_index(self, symbol, name):
        index = self.model(
            symbol=symbol,
            name=name
        )
        index.save(using=self._db)

        return index

    def create_index(self, symbol, name):
        return self._create_index(symbol, name)

    def with_stock_count(self):
        """
        Method to get all index objects and the number of stock constituents
        """
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT i.id, i.symbol, i.name, COUNT(*)
            FROM fintrack_be_index i, fintrack_be_indexconstituents c
            WHERE i.id = c.index_id
            GROUP BY i.id, i.symbol
            ORDER BY i.symbol DESC""")
            result_list = []

            for row in cursor.fetchall():
                e = self.model(id=row[0],
                               symbol=row[1],
                               name=row[2])
                e.num_stocks = row[3]
                result_list.append(e)

            return result_list