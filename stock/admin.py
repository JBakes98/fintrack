from django.contrib import admin
from stock.models import Stock, StockPriceData


class StockAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'ticker',
            'name',
            'company',
            'exchange',
        )}),
    )

    list_display = ('ticker', 'name', 'company', 'exchange')
    list_filter = ('exchange', 'company__industry__sector', 'company__industry', 'company')
    search_fields = ('ticker',)
    ordering = ('ticker',)


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


admin.site.register(Stock, StockAdmin)
admin.site.register(StockPriceData, StockPriceAdmin)