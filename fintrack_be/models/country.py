from django.db import models

from fintrack_be.managers.country_manager import CountryManager


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    alpha2 = models.CharField(max_length=2, unique=True, blank=False, null=False)
    alpha3 = models.CharField(max_length=3, unique=True, blank=True, null=True)
    numeric = models.IntegerField(unique=True, blank=True, null=True)

    objects = CountryManager()

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = "Countries"
        ordering = ['alpha2', ]

    def __str__(self):
        return self.alpha2

    def __unicode__(self):
        return self.alpha2
