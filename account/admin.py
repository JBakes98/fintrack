from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

UserModel = get_user_model()


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': (
            'email',
            'password',
            'first_name',
            'last_name',
            'country',
            'timezone',
            'last_login'
        )}),
        ('Permissions', {'fields': (
            'is_verified',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )

    list_display = ('email',
                    'first_name',
                    'last_name',
                    'country',
                    'timezone',
                    'is_verified',
                    'is_staff',
                    'is_superuser',
                    'last_login')

    list_filter = ('country',
                   'timezone',
                   'is_staff',
                   'is_superuser',
                   'is_active',
                   'groups')

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(UserModel, UserAdmin)
