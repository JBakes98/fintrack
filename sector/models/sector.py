from django.db import models


class Sector(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'

    def __str__(self):
        return self.name

    def industry_count(self):
        return self.industry_sector.count()

    def company_count(self):
        count = 0
        industries = self.industry_sector.all()
        for industry in industries:
            count += industry.company_industry.count()
        return count
