from django.core.management import BaseCommand
from index.utils import seed_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        seed_data.create_indices()
        seed_data.create_constituents()

