from django.contrib import admin

from fintrack_be.models import IndexPriceData


class IndexPriceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'timestamp',
            'index',
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
                    'index',
                    'open',
                    'close',
                    'change',
                    'change_perc',
                    'volume')
    list_filter = ('index', )
    search_fields = ('index', 'timestamp')
    ordering = ('index', '-timestamp')


admin.site.register(IndexPriceData, IndexPriceAdmin)