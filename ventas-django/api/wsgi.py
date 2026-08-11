"""
WSGI config for Ventas Ingenio.
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

from django.core.wsgi import get_wsgi_application

from api.middleware.auto_migrate import apply_pending_migrations

app = get_wsgi_application()

# Intento temprano en cold start; no debe tumbar el import del módulo WSGI.
try:
    apply_pending_migrations()
except Exception:
    pass
