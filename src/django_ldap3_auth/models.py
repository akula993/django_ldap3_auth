from django.core.exceptions import ValidationError
from django.db import models


class LDAPConfig(models.Model):
    singleton = models.BooleanField(default=True, editable=False)


    host = models.CharField(max_length=255, default='localhost')
    port = models.IntegerField(default=389)
    use_ssl = models.BooleanField(default=False)
    base_dn = models.CharField(max_length=512, blank=True, default='')

    bind_dn = models.CharField(max_length=512, blank=True, null=True)
    bind_password = models.CharField(max_length=512, blank=True, null=True,
                                     help_text='Храните секреты в переменных окружения, это поле только для тестов.')

    search_filter = models.CharField(max_length=512, default='(&(objectClass=user)(sAMAccountName={username}))')
    search_attrs = models.JSONField(default=list)

    default_email_domain = models.CharField(max_length=255, blank=True, null=True)
    map_first_name = models.CharField(max_length=64, default='givenName')
    map_last_name = models.CharField(max_length=64, default='sn')

    superuser_group = models.CharField(max_length=512, blank=True, null=True)
    staff_group = models.CharField(max_length=512, blank=True, null=True)


    class Meta:
        verbose_name = 'LDAP конфигурация'
        verbose_name_plural = 'LDAP конфигурация (одна запись)'

        def clean(self):
            if LDAPConfig.objects.exclude(pk=self.pk).exists():
                raise ValidationError('Допускается только одна запись LDAPConfig.')

        def __str__(self):
            return f"LDAP @ {self.host}:{self.port}"

        @classmethod
        def to_conf(cls, base_conf):
            """Слить base_conf (из settings.py) с записью из БД при наличии."""
            try:
                cfg = cls.objects.get()
            except cls.DoesNotExist:
                return base_conf
            base_conf.host = cfg.host
            base_conf.port = cfg.port
            base_conf.use_ssl = cfg.use_ssl
            base_conf.base_dn = cfg.base_dn
            base_conf.bind_dn = cfg.bind_dn or base_conf.bind_dn
            base_conf.bind_password = cfg.bind_password or base_conf.bind_password
            base_conf.search_filter = cfg.search_filter
            base_conf.search_attrs = cfg.search_attrs or base_conf.search_attrs
            base_conf.default_email_domain = cfg.default_email_domain or base_conf.default_email_domain
            base_conf.map_first_name = cfg.map_first_name or base_conf.map_first_name
            base_conf.map_last_name = cfg.map_last_name or base_conf.map_last_name
            base_conf.superuser_group = cfg.superuser_group or base_conf.superuser_group
            base_conf.staff_group = cfg.staff_group or base_conf.staff_group
            return base_conf
