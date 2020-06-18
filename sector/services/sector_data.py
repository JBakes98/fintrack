from sector.models import Sector


def create_sector(name):
    """
    Method that creates a Sector
    :param name: Sector name
    """
    Sector.objects.update_or_create(name=name)
    print('{} created'.format(name))
