from django.contrib import admin

from fintrack_be.models import Company


class CompanyAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'short_name',
            'long_name',
        )}),
        ('Buisness Summary', {'fields': (
            'industry',
            'business_summary'
        )}),
        ('Company Shares', {'fields': (

         )}),
    )

    list_display = ('short_name', 'long_name', 'industry')
    list_filter = ('industry__sector', 'industry',)
    search_fields = ('short_name', 'long_name')
    ordering = ('short_name',)


admin.site.register(Company, CompanyAdmin)
