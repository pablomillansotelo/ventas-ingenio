"""SQL idempotente para alinear Neon/init.sql legacy con el modelo Django actual."""

ENSURE_POSTGRES_SCHEMA_SQL = [
    """
    CREATE TABLE IF NOT EXISTS cat_vendedor (
        id_vendedor SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL UNIQUE,
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(254) NOT NULL DEFAULT '',
        telefono VARCHAR(15),
        comision_pct NUMERIC(5, 2) NOT NULL DEFAULT 0,
        activo BOOLEAN NOT NULL DEFAULT TRUE
    );
    """,
    "ALTER TABLE cat_vendedor ADD COLUMN IF NOT EXISTS comision_pct NUMERIC(5, 2) NOT NULL DEFAULT 0;",
    "ALTER TABLE cat_cliente ADD COLUMN IF NOT EXISTS curp VARCHAR(18);",
    "ALTER TABLE cat_cliente ADD COLUMN IF NOT EXISTS empresa VARCHAR(100);",
    "ALTER TABLE cat_cliente ADD COLUMN IF NOT EXISTS id_alumno_sii INTEGER;",
    "ALTER TABLE cat_cliente ADD COLUMN IF NOT EXISTS notas TEXT NOT NULL DEFAULT '';",
    "ALTER TABLE cat_cliente ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT TRUE;",
    "ALTER TABLE cat_cliente ALTER COLUMN direccion TYPE VARCHAR(120);",
    "ALTER TABLE cat_cliente ALTER COLUMN email TYPE VARCHAR(254);",
    "ALTER TABLE cat_producto ADD COLUMN IF NOT EXISTS codigo VARCHAR(20);",
    "ALTER TABLE cat_producto ADD COLUMN IF NOT EXISTS descripcion TEXT NOT NULL DEFAULT '';",
    "ALTER TABLE cat_producto ADD COLUMN IF NOT EXISTS duracion_horas SMALLINT;",
    "ALTER TABLE cat_producto ADD COLUMN IF NOT EXISTS modalidad VARCHAR(20) NOT NULL DEFAULT 'online';",
    "ALTER TABLE cat_producto ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT TRUE;",
    "ALTER TABLE cat_producto ALTER COLUMN producto TYPE VARCHAR(120);",
    """
    CREATE TABLE IF NOT EXISTS cat_edicion_curso (
        id_edicion SERIAL PRIMARY KEY,
        id_curso INTEGER NOT NULL REFERENCES cat_producto(id_producto),
        codigo_edicion VARCHAR(30) NOT NULL UNIQUE,
        fecha_inicio DATE NOT NULL,
        fecha_fin DATE,
        cupo_maximo SMALLINT NOT NULL DEFAULT 20,
        cupo_ocupado SMALLINT NOT NULL DEFAULT 0,
        precio_edicion NUMERIC(19, 4),
        estado VARCHAR(20) NOT NULL DEFAULT 'programada',
        activo BOOLEAN NOT NULL DEFAULT TRUE
    );
    """,
    "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS id_vendedor INTEGER REFERENCES cat_vendedor(id_vendedor);",
    "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS folio VARCHAR(20) UNIQUE;",
    "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS estado VARCHAR(20) NOT NULL DEFAULT 'confirmada';",
    "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS estado_pago VARCHAR(20) NOT NULL DEFAULT 'pendiente';",
    "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS observaciones TEXT NOT NULL DEFAULT '';",
    "ALTER TABLE tra_venta ADD COLUMN IF NOT EXISTS registrado_en TIMESTAMPTZ;",
    "ALTER TABLE tra_venta_det ADD COLUMN IF NOT EXISTS precio_unitario NUMERIC(19, 4);",
    "ALTER TABLE tra_venta_det ADD COLUMN IF NOT EXISTS id_edicion INTEGER REFERENCES cat_edicion_curso(id_edicion);",
    """
    CREATE TABLE IF NOT EXISTS tra_pago (
        id_pago SERIAL PRIMARY KEY,
        id_venta INTEGER NOT NULL REFERENCES tra_venta(id_venta),
        monto NUMERIC(19, 4) NOT NULL,
        metodo VARCHAR(20) NOT NULL DEFAULT 'transferencia',
        referencia VARCHAR(60) NOT NULL DEFAULT '',
        fecha_pago TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        estado VARCHAR(20) NOT NULL DEFAULT 'aplicado'
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS tra_inscripcion (
        id_inscripcion SERIAL PRIMARY KEY,
        id_cliente INTEGER NOT NULL REFERENCES cat_cliente(id_cliente),
        id_curso INTEGER NOT NULL REFERENCES cat_producto(id_producto),
        id_edicion INTEGER REFERENCES cat_edicion_curso(id_edicion),
        id_venta_det INTEGER REFERENCES tra_venta_det(id_venta_det),
        estado VARCHAR(20) NOT NULL DEFAULT 'activa',
        fecha_inscripcion TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        id_alumno_externo INTEGER
    );
    """,
    """
    UPDATE cat_producto
    SET codigo = 'CURSO-' || id_producto
    WHERE codigo IS NULL OR codigo = '';
    """,
    """
    UPDATE tra_venta
    SET folio = 'V-' || LPAD(id_venta::text, 6, '0')
    WHERE folio IS NULL OR folio = '';
    """,
]


def ensure_postgres_schema(connection):
    if connection.vendor != 'postgresql':
        return

    with connection.cursor() as cursor:
        for sql in ENSURE_POSTGRES_SCHEMA_SQL:
            cursor.execute(sql)
