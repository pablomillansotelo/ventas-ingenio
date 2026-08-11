-- Ventas Ingenio: esquema de la base de datos de negocio (default)
-- Compatible con ventas-django/ventas/models.py

CREATE TABLE IF NOT EXISTS cat_cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    direccion VARCHAR(120) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL,
    telefono VARCHAR(15),
    curp VARCHAR(18),
    empresa VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS cat_vendedor (
    id_vendedor SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL DEFAULT '',
    telefono VARCHAR(15),
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS cat_producto (
    id_producto SERIAL PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    producto VARCHAR(120) NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    duracion_horas SMALLINT,
    modalidad VARCHAR(20) NOT NULL DEFAULT 'online',
    precio_unitario NUMERIC(19, 4) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS tra_venta (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES cat_cliente(id_cliente),
    id_vendedor INTEGER REFERENCES cat_vendedor(id_vendedor),
    fecha DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'confirmada',
    observaciones TEXT NOT NULL DEFAULT '',
    registrado_en TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS tra_venta_det (
    id_venta_det SERIAL PRIMARY KEY,
    id_venta INTEGER NOT NULL REFERENCES tra_venta(id_venta),
    id_producto INTEGER NOT NULL REFERENCES cat_producto(id_producto),
    cantidad INTEGER NOT NULL DEFAULT 1,
    precio_unitario NUMERIC(19, 4),
    descuento NUMERIC(19, 4),
    UNIQUE (id_venta, id_producto)
);

CREATE INDEX IF NOT EXISTS idx_tra_venta_cliente ON tra_venta(id_cliente);
CREATE INDEX IF NOT EXISTS idx_tra_venta_vendedor ON tra_venta(id_vendedor);
CREATE INDEX IF NOT EXISTS idx_tra_venta_det_venta ON tra_venta_det(id_venta);
CREATE INDEX IF NOT EXISTS idx_tra_venta_det_producto ON tra_venta_det(id_producto);
