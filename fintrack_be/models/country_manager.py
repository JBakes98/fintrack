from django.db import models


class CountryManager(models.Manager):
    use_in_migrations = True

    def _create_country(self, name, alpha2, alpha3, numeric):
        country = self.model(
            name=name,
            alpha2=alpha2,
            alpha3=alpha3,
            numeric=numeric
        )
        country.save(using=self._db)

        return country

    def create_country(self, name, alpha2, alpha3, numeric):
        return self._create_country(name, alpha2, alpha3, numeric)
