from django.db import models


class Sector(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def industry_count(self):
        return self.sector_industries.count()

    def company_count(self):
        count = 0
        industries = self.sector_industries.all()
        for industry in industries:
            count += industry.industry_companies.count()
        return count
