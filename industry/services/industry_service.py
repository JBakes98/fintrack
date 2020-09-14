from sector.models import Sector
from industry.models import Industry


class IndustryService:
    @staticmethod
    def create_industry(name, sector):
        """
        Method to create an Industry taking individual parameters, if parent Sector
        does not exist then it creates the Sector
        :param name: Industry name
        :param sector: Industries parent Sector
        """
        try:
            sector = Sector.objects.get(name=sector)
            Industry.objects.update_or_create(name=name, sector=sector)
            print('{} created'.format(name))

        except Sector.DoesNotExist as e:
            print('{}: {}'.format(sector, e))
            sector = Sector.objects.create_sector(sector)
            Industry.objects.update_or_create(name=name, sector=sector)
            print('{} created'.format(name))
