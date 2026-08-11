from django.db import migrations

from api.db_schema import ensure_postgres_schema


def _ensure_postgres_schema(apps, schema_editor):
    ensure_postgres_schema(schema_editor.connection)


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0002_dominio_cursos_vendedores'),
    ]

    operations = [
        migrations.RunPython(_ensure_postgres_schema, migrations.RunPython.noop),
    ]
