# Ventas Ingenio

## Descripción General

**Ventas Ingenio** es un sistema integral de gestión de ventas diseñado para administrar eficientemente clientes, productos, inventarios y transacciones de venta. Este proyecto no solo sirve como un punto de venta (POS), sino que también integra lógica de negocio para conectar con otros sistemas educativos (como un SII - Sistema Integral de Información).

## Funcionalidades de Negocio

El sistema permite realizar las siguientes operaciones clave:

*   **Gestión de Clientes**: Registro, edición, eliminación y consulta de clientes. Además, cuenta con una integración que intenta registrar automáticamente al cliente como alumno en un sistema externo (SII).
*   **Gestión de Productos e Inventario**: Administración del catálogo de productos, precios unitarios y control de inventario.
*   **Punto de Venta y Carrito**: Funcionalidad para agregar productos a un carrito de compras y registrar ventas.
*   **Registro de Ventas**: Histórico de ventas realizadas con detalle de productos y montos.

## Aspectos Técnicos

El proyecto está construido principalmente utilizando **Python** y el framework **Django**.

### Arquitectura

*   **Backend**: Django (Python).
*   **Base de Datos**: PostgreSQL (utilizando `psycopg2`). El sistema está configurado para manejar múltiples bases de datos (una para autenticación y otra para la lógica de negocio).
*   **Integración**: Módulo de servicios para conectar con APIs externas (SII API, Aula API).
*   **Frontend**: Plantillas de Django (Django Templates) con archivos estáticos (CSS/JS).

### Estructura del Repositorio

El repositorio se divide en las siguientes secciones:

*   **`ventas-django/`**: Contiene el código fuente principal del proyecto Django.
    *   Lógica de la aplicación (`ventas`).
    *   Configuración del proyecto (`api`).
    *   Plantillas y archivos estáticos.
*   **`ventas-sql/`**: Contiene scripts SQL para inicialización o mantenimiento de la base de datos (por ejemplo, `init.sql`).

## Documentación Detallada

Para obtener información más técnica y específica sobre cómo levantar el proyecto, por favor consulta la documentación dentro de la carpeta `ventas-django` y sus subdirectorios de documentación.
