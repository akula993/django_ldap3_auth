from django.core.management.base import BaseCommand

from src.django_ldap3_auth.backends import LDAPBackend


class Command(BaseCommand):
    help = 'Проверить LDAP‑подключение и поиск пользователя.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True)
        parser.add_argument('--password', required=True)

    def handle(self, *args, **opts):
        backend = LDAPBackend()
        user = backend.authenticate(None, username=opts['username'], password=opts['password'])
        if user:
            self.stdout.write(self.style.SUCCESS(f"OK: вошёл как {user.username} (id={user.id})"))
        else:
            self.stdout.write(self.style.ERROR('FAIL: аутентификация не удалась'))
