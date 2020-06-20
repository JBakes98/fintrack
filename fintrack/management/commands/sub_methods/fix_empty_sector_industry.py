from sector.models import Sector
from industry.models import Industry
from company.models import Company


def fix():
    sector = Sector.objects.get(pk=7)
    industry = Industry.objects.get(pk=24)
    companies = Company.objects.filter(industry=industry)

    for company in companies:
        company.industry = Industry.objects.get(pk=1)
        company.save()

    sector.delete()
    industry.delete()

