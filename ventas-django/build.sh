#!/usr/bin/env bash
set -euo pipefail

pip install -r requirements.txt
python manage.py collectstatic --noinput

# Las migraciones se aplican en api/wsgi.py al arrancar (runtime),
# porque en Vercel las variables de BD no suelen estar en el build.
