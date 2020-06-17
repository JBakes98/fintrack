from django.db import models
from sector.models.sector import Sector


class Industry(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='industry_sector')

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'
        db_table = 'industry'

    def __str__(self):
        return self.name

    def industry_company_count(self):
        return self.company_industry.count()