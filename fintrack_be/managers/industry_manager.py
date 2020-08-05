from django.db import models

from fintrack_be.models.sector import Sector


class IndustryManager(models.Manager):
    use_in_migrations = True

    def _create_industry(self, name, sector):
        try:
            sector = Sector.objects.get(name=sector)
        except Sector.DoesNotExist:
            sector = Sector.objects.create_sector(sector)
        industry = self.model(
            name=name,
            sector=sector
        )
        industry.save()

        return industry

    def create_industry(self, name, sector):
        return self._create_industry(name, sector)
