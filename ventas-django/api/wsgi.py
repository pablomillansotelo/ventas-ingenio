"""
WSGI config for Ventas Ingenio.

En Vercel las credenciales de Postgres suelen estar disponibles solo en runtime,
no durante el build. Por eso las migraciones se aplican al arrancar cada instancia.
"""

import logging
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

logger = logging.getLogger(__name__)

_migrations_done = False


def _apply_migrations():
    global _migrations_done
    if _migrations_done:
        return

    from django.core.management import call_command

    call_command('migrate', '--noinput', verbosity=0)
    call_command('migrate', '--database=auth', '--noinput', verbosity=0)
    _migrations_done = True
    logger.info('Migraciones aplicadas (default + auth)')


from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()

try:
    _apply_migrations()
except Exception:
    logger.exception('No se pudieron aplicar las migraciones al iniciar la app')
