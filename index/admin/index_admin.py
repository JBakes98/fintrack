from django.contrib import admin

from index.models import Index


class ConstituentInlineAdmin(admin.TabularInline):
    model = Index.constituents.through


class IndexAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'symbol',
            'name',
        )}),
    )

    inlines = (ConstituentInlineAdmin, )
    list_display = ('symbol', 'name', 'constituents_count')
    search_fields = ('symbol', 'name')
    ordering = ('symbol',)


admin.site.register(Index, IndexAdmin)
