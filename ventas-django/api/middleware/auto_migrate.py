import logging
import threading

from django.core.management import call_command
from django.db import connection

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_migrations_applied = False

_ENSURE_VENDEDOR_SQL = """
CREATE TABLE IF NOT EXISTS cat_vendedor (
    id_vendedor SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL DEFAULT '',
    telefono VARCHAR(15),
    activo BOOLEAN NOT NULL DEFAULT TRUE
);
"""

_ENSURE_VENTA_COLUMNS_SQL = [
    "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS id_vendedor INTEGER REFERENCES cat_vendedor(id_vendedor);",
    "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS estado VARCHAR(20) NOT NULL DEFAULT 'confirmada';",
    "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS observaciones TEXT NOT NULL DEFAULT '';",
    "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS registrado_en TIMESTAMPTZ;",
]


def _ensure_minimum_schema():
    """Respaldo idempotente por si migrate no pudo completar 0002 en Neon."""
    if connection.vendor != 'postgresql':
        return

    with connection.cursor() as cursor:
        cursor.execute(_ENSURE_VENDEDOR_SQL)
        for sql in _ENSURE_VENTA_COLUMNS_SQL:
            cursor.execute(sql)


def apply_pending_migrations():
    """Aplica migraciones pendientes una vez por instancia serverless."""
    global _migrations_applied
    if _migrations_applied:
        return

    with _lock:
        if _migrations_applied:
            return

        # --fake-initial: tablas creadas con init.sql → salta 0001 y aplica 0002+
        call_command('migrate', '--noinput', '--fake-initial', verbosity=1)
        call_command('migrate', '--database=auth', '--noinput', '--fake-initial', verbosity=1)
        _ensure_minimum_schema()
        _migrations_applied = True
        logger.info('Migraciones y esquema mínimo verificados')


class AutoMigrateMiddleware:
    """Ejecuta migrate en la primera petición HTTP (runtime Vercel con credenciales Neon)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        apply_pending_migrations()
        return self.get_response(request)
