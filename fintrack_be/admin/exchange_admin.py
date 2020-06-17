from django.contrib import admin

from fintrack_be.models import Exchange


class ExchangeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'symbol',
            'name',
            'opening_time',
            'closing_time',
        )}),
        ('Location', {'fields': (
            'country',
            'timezone',
        )}),
    )

    list_display = ('symbol', 'name', 'country', 'timezone', 'opening_time',
                    'closing_time', 'market_open')
    list_filter = ('timezone', 'country',)
    search_fields = ('symbol', 'name')
    ordering = ('symbol',)


admin.site.register(Exchange, ExchangeAdmin)
