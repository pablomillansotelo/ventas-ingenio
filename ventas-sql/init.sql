-- Ventas Ingenio: esquema de la base de datos de negocio (default)
-- Compatible con ventas-django/ventas/models.py
-- Ejecutar contra la base configurada en DB_NAME

CREATE TABLE IF NOT EXISTS cat_cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    direccion VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL,
    telefono VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS cat_producto (
    id_producto SERIAL PRIMARY KEY,
    producto VARCHAR(40) NOT NULL,
    precio_unitario NUMERIC(19, 4) NOT NULL
);

CREATE TABLE IF NOT EXISTS tra_venta (
    id_venta SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES cat_cliente(id_cliente),
    fecha DATE
);

CREATE TABLE IF NOT EXISTS tra_venta_det (
    id_venta_det SERIAL PRIMARY KEY,
    id_venta INTEGER NOT NULL REFERENCES tra_venta(id_venta),
    id_producto INTEGER NOT NULL REFERENCES cat_producto(id_producto),
    cantidad INTEGER NOT NULL,
    descuento NUMERIC(19, 4),
    UNIQUE (id_venta, id_producto)
);

CREATE INDEX IF NOT EXISTS idx_tra_venta_cliente ON tra_venta(id_cliente);
CREATE INDEX IF NOT EXISTS idx_tra_venta_det_venta ON tra_venta_det(id_venta);
CREATE INDEX IF NOT EXISTS idx_tra_venta_det_producto ON tra_venta_det(id_producto);
