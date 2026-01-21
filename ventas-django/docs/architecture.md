# Arquitectura del Sistema

## Estructura General

El proyecto sigue el patrón MVT (Model-View-Template) estándar de Django, pero introduce una arquitectura de múltiples bases de datos para separar preocupaciones.

### Estructura de Directorios

*   `api/`: Configuración del proyecto.
*   `ventas/`: Aplicación principal.
*   `dbrouters/`: Lógica de enrutamiento de DB.

## Modelos de Datos (`ventas`)

La aplicación `ventas` gestiona la lógica de negocio principal. Sus modelos residen en la base de datos `default`.

### 1. Cliente (`cat_cliente`)
Almacena la información de los clientes.
*   `id_cliente`: PK
*   `nombre`, `apellidos`, `direccion`, `email`, `telefono`

### 2. Producto (`cat_producto`)
Catálogo de productos disponibles.
*   `id_producto`: PK
*   `producto`: Nombre del producto
*   `precio_unitario`: Precio decimal

### 3. Venta (`tra_venta`)
Cabecera de una transacción de venta.
*   `id_venta`: PK
*   `id_cliente`: FK a Cliente
*   `fecha`: Fecha de la venta

### 4. VentaDetalle (`tra_venta_det`)
Detalle de productos por venta.
*   `id_venta`: FK a Venta
*   `id_producto`: FK a Producto
*   `cantidad`: Cantidad vendida
*   `descuento`: Descuento aplicado

## Estrategia de Múltiples Bases de Datos

El sistema utiliza un **Database Router** personalizado (`api.dbrouters.auth_router.AuthRouter`) para dirigir las operaciones de base de datos.

*   **Base de Datos `auth`**: Se utiliza para las aplicaciones de sistema de Django:
    *   `auth` (Usuarios, Grupos)
    *   `admin` (Interfaz administrativa)
    *   `sessions` (Sesiones de usuario)
    *   `contenttypes`

*   **Base de Datos `default`**: Se utiliza para todo lo demás, específicamente la aplicación `ventas`.

Esto permite que la información de usuarios del sistema esté desacoplada de la información transaccional del negocio.

## Frontend

El frontend se sirve directamente desde Django utilizando **Django Templates**.
*   Las plantillas base se encuentran en `templates/`.
*   Los archivos estáticos (CSS, JS) se encuentran en `static/`.
*   Se utiliza `whitenoise` para servir archivos estáticos en producción.
