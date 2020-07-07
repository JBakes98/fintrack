from django.contrib import admin

from fintrack_be.models import EmailTemplate


class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EmailTemplate._meta.fields if field.name != 'id']
    search_fields = ('subject', 'html_template')
    ordering = ('html_template', )


admin.site.register(EmailTemplate, EmailTemplateAdmin)
