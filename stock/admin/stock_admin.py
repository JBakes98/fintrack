from django.contrib import admin
from stock.models import Stock


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


admin.site.register(Stock, StockAdmin)
