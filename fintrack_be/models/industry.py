from django.db import models

from fintrack_be.models.sector import Sector
from fintrack_be.models.industry_manager import IndustryManager


class Industry(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='sector_industries')

    objects = IndustryManager()

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'
        ordering = ['sector', 'name']

    def __str__(self):
        return self.name

    @property
    def company_count(self):
        return self.industry_companies.count()