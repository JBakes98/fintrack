from sector.models import Sector
from industry.models import Industry


class IndustryService:
    def __init__(self, name, sector):
        self._name = name
        self._sector = sector

    def create_industry(self):
        """
        Method to create an Industry taking individual parameters, if parent Sector
        does not exist then it creates the Sector
        :param name: Industry name
        :param sector: Industries parent Sector
        """
        try:
            sector_obj = Sector.objects.get(name=self._sector)
            Industry.objects.update_or_create(name=self._name, sector=sector_obj)
            print('{} created'.format(self._name))

        except Sector.DoesNotExist as e:
            print('{}: {}'.format(self._sector, e))
            sector = Sector.objects.create_sector(self._sector)
            Industry.objects.update_or_create(name=self._name, sector=sector)
            print('{} created'.format(self._name))
