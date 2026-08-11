import logging
import threading

from django.core.management import call_command
from django.db import connection

from api.db_schema import ensure_postgres_schema

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_schema_checked = False
_migrate_done = False


def _ensure_minimum_schema():
    """Respaldo idempotente por si migrate no pudo completar 0002/0003 en Neon."""
    ensure_postgres_schema(connection)


def apply_pending_migrations():
    """Aplica migraciones pendientes una vez por instancia serverless."""
    global _schema_checked, _migrate_done

    if not _schema_checked:
        with _lock:
            if not _schema_checked:
                _ensure_minimum_schema()
                _schema_checked = True

    if _migrate_done:
        return

    with _lock:
        if _migrate_done:
            return

        _ensure_minimum_schema()
        try:
            # --fake-initial: tablas creadas con init.sql → salta 0001 y aplica 0002+
            call_command('migrate', '--noinput', '--fake-initial', verbosity=1)
            call_command('migrate', '--database=auth', '--noinput', '--fake-initial', verbosity=1)
            logger.info('Migraciones aplicadas correctamente')
        except Exception:
            logger.exception('No se pudieron aplicar las migraciones al iniciar la app')
        finally:
            _ensure_minimum_schema()
            _migrate_done = True


class AutoMigrateMiddleware:
    """Ejecuta migrate en la primera petición HTTP (runtime Vercel con credenciales Neon)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        apply_pending_migrations()
        return self.get_response(request)
