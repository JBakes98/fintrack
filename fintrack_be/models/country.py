from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    alpha2 = models.CharField(max_length=2, unique=True, blank=False, null=False)
    alpha3 = models.CharField(max_length=3, unique=True, blank=True, null=True)
    numeric = models.IntegerField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = "Countries"
        db_table = 'country'

    def __str__(self):
        return self.alpha2
