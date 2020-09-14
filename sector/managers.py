from django.db import models


class SectorManager(models.Manager):
    use_in_migration = True

    def _create_sector(self, name):
        sector = self.model(
            name=name
        )
        sector.save()

        return sector

    def create_sector(self, name):
        return self._create_sector(name)
