from django.db import migrations, models


def create_singleton(apps, schema_editor):
    LDAPConfig = apps.get_model('django_ldap3_auth', 'LDAPConfig')
    if not LDAPConfig.objects.exists():
        LDAPConfig.objects.create(search_attrs=['cn', 'mail', 'givenName', 'sn', 'memberOf', 'userPrincipalName'])


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='LDAPConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('singleton', models.BooleanField(default=True, editable=False)),
                ('host', models.CharField(default='localhost', max_length=255)),
                ('port', models.IntegerField(default=389)),
                ('use_ssl', models.BooleanField(default=False)),
                ('base_dn', models.CharField(blank=True, default='', max_length=512)),
                ('bind_dn', models.CharField(blank=True, max_length=512, null=True)),
                ('bind_password', models.CharField(blank=True,
                                                   help_text='Храните секреты в переменных окружения, это поле только для тестов.',
                                                   max_length=512, null=True)),
                ('search_filter',
                 models.CharField(default='(&(objectClass=user)(sAMAccountName={username}))', max_length=512)),
                ('search_attrs', models.JSONField(default=list)),
                ('default_email_domain', models.CharField(blank=True, max_length=255, null=True)),
                ('map_first_name', models.CharField(default='givenName', max_length=64)),
                ('map_last_name', models.CharField(default='sn', max_length=64)),
                ('superuser_group', models.CharField(blank=True, max_length=512, null=True)),
                ('staff_group', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'verbose_name': 'LDAP конфигурация',
                'verbose_name_plural': 'LDAP конфигурация (одна запись)',
            },
        ),
        migrations.RunPython(create_singleton, migrations.RunPython.noop),
    ]
