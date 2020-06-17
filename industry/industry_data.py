from industry.models import Industry
from sector.models import Sector
from sector import sector_data


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
        sector_data.create_sector(sector)
        sector = Sector.objects.get(name=sector)
        Industry.objects.update_or_create(name=name, sector=sector)
        print('{} created'.format(name))