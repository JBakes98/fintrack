from django.contrib import admin
from fintrack_be.admin.linkify import linkify
from fintrack_be.models import Stock


class StockAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'ticker',
            'name',
            'company',
            'exchange',
        )}),
    )

    list_display = ('ticker', 'name', linkify(field_name='company'), linkify(field_name='exchange'))
    list_filter = ('exchange', 'company__industry__sector', 'company__industry', 'company')
    search_fields = ('ticker',)
    ordering = ('ticker',)


admin.site.register(Stock, StockAdmin)
