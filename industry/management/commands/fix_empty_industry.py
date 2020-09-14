from django.core.management import BaseCommand
from django.db.backends.utils import logger


from industry.models import Industry
from company.models import Company


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('Correcting Industry data...')
        industry = Industry.objects.get(pk=24)
        companies = Company.objects.filter(industry=industry)

        for company in companies:
            company.industry = Industry.objects.get(pk=1)
            company.save()

        industry.delete()
        logger.info('Finished changes.')
