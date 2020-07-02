from django.contrib import admin

from fintrack_be.models import Position


class PositionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'instrument',
            'user',
        )}),
        ('Position Summary', {'fields': (
            'open_date',
            'open_price',
            'close_date',
            'close_price',
            'quantity',
            'result',
            'direction',
        )}),
    )

    list_display = ('id', 'instrument', 'user', 'open_date', 'close_date', 'is_open', 'direction')
    list_filter = ('instrument', 'user', 'direction')
    search_fields = ('instrument', 'user')
    ordering = ('instrument', 'user', 'open_date', 'direction')


admin.site.register(Position, PositionAdmin)