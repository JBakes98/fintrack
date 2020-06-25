from django.contrib import admin
from fintrack_be.models import EmailList


class RecipientInlineAdmin(admin.TabularInline):
    model = EmailList.recipients.through
    extra = 0


class EmailListAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'name',
            'description',
            'template',
            'send_time',
            'send_days',
        )}),
    )

    inlines = (RecipientInlineAdmin, )
    list_display = ('name', 'recipient_count')
    search_fields = ('name', )
    ordering = ('name', )


admin.site.register(EmailList, EmailListAdmin)
