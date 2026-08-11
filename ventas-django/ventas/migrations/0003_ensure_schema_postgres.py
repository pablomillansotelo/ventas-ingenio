from django.db import migrations


def ensure_postgres_schema(apps, schema_editor):
    if schema_editor.connection.vendor != 'postgresql':
        return

    statements = [
        """
        CREATE TABLE IF NOT EXISTS cat_vendedor (
            id_vendedor SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL UNIQUE,
            nombre VARCHAR(100) NOT NULL,
            email VARCHAR(254) NOT NULL DEFAULT '',
            telefono VARCHAR(15),
            activo BOOLEAN NOT NULL DEFAULT TRUE
        );
        """,
        "ALTER TABLE cat_cliente ADD COLUMN IF NOT EXISTS curp VARCHAR(18);",
        "ALTER TABLE cat_cliente ADD COLUMN IF NOT EXISTS empresa VARCHAR(100);",
        "ALTER TABLE cat_producto ADD COLUMN IF NOT EXISTS codigo VARCHAR(20);",
        "ALTER TABLE cat_producto ADD COLUMN IF NOT EXISTS descripcion TEXT NOT NULL DEFAULT '';",
        "ALTER TABLE cat_producto ADD COLUMN IF NOT EXISTS duracion_horas SMALLINT;",
        "ALTER TABLE cat_producto ADD COLUMN IF NOT EXISTS modalidad VARCHAR(20) NOT NULL DEFAULT 'online';",
        "ALTER TABLE cat_producto ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT TRUE;",
        "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS id_vendedor INTEGER REFERENCES cat_vendedor(id_vendedor);",
        "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS estado VARCHAR(20) NOT NULL DEFAULT 'confirmada';",
        "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS observaciones TEXT NOT NULL DEFAULT '';",
        "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS registrado_en TIMESTAMPTZ;",
        "ALTER TABLE tra_venta_det ADD COLUMN IF NOT EXISTS precio_unitario NUMERIC(19, 4);",
        """
        UPDATE cat_producto
        SET codigo = 'CURSO-' || id_producto
        WHERE codigo IS NULL OR codigo = '';
        """,
    ]

    with schema_editor.connection.cursor() as cursor:
        for sql in statements:
            cursor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0002_dominio_cursos_vendedores'),
    ]

    operations = [
        migrations.RunPython(ensure_postgres_schema, migrations.RunPython.noop),
    ]
