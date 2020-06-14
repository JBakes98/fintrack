from django.db import models


class Sector(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectors'
        db_table = 'sector'

    def __str__(self):
        return self.name

    def sub_industry_count(self):
        return self.industry_sector.count()

    def sector_constituents(self):
        constituents = 0
        industries = self.industry_sector.all()
        for industry in industries:
            constituents += industry.company_industry.count()
        return constituents
