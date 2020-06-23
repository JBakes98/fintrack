from django.core.management.base import BaseCommand
from fintrack_be.models import Company


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(Company.objects.get(short_name='American Airlines Group Inc.').get_absolute_url())
        print(Company.objects.get(short_name='Apple Inc.').get_absolute_url())
