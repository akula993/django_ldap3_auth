from django.contrib import admin

from .models import LDAPConfig


@admin.register(LDAPConfig)
class LDAPConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('host', 'port', 'use_ssl', 'base_dn')}),
        ('Bind учётка', {'fields': ('bind_dn', 'bind_password')}),
        ('Поиск пользователя', {'fields': ('search_filter', 'search_attrs')}),
        ('Маппинг атрибутов', {'fields': ('default_email_domain', 'map_first_name', 'map_last_name')}),
        ('Группы и роли', {'fields': ('superuser_group', 'staff_group')}),
    )
    readonly_fields = ()

    def get_readonly_fields(self, request, obj=None):
        # Можно сделать только просмотр (например на проде)
        return super().get_readonly_fields(request, obj)
