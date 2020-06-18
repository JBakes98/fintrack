from django.contrib import admin

from stock.models import StockPriceData


class StockPriceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'timestamp',
            'stock',
        )}),
        ('Data', {'fields': (
            'open',
            'low',
            'high',
            'close',
            'volume',
            'change',
            'change_perc'
        )}),
    )

    list_display = ('timestamp',
                    'stock',
                    'open',
                    'close',
                    'change',
                    'change_perc',
                    'volume')
    list_filter = ('stock', )
    search_fields = ('stock', 'timestamp')
    ordering = ('stock', '-timestamp')


admin.site.register(StockPriceData, StockPriceAdmin)