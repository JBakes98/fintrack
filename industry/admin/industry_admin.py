from django.contrib import admin

from industry.models import Industry


class IndustryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'name',
            'sector'
        )}),
    )

    list_display = ('name', 'sector',)
    list_filter = ('sector',)
    search_fields = ('name', 'sector')
    ordering = ('name',)


admin.site.register(Industry, IndustryAdmin)
