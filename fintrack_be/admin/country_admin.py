from django.contrib import admin
from fintrack_be.models import Country


class CountryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'name',
            'alpha2',
            'alpha3',
            'numeric'
        )}),
    )

    list_display = ('name', 'alpha2', 'alpha3', 'numeric')
    search_fields = ('name', 'alpha2', 'alpha3', 'numeric')
    ordering = ('alpha2',)


admin.site.register(Country, CountryAdmin)
