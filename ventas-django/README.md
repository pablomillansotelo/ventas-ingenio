# Ventas Django Project

Este directorio contiene el código fuente de la aplicación web basada en Django para el sistema **Ventas Ingenio**.

## Descripción Técnica Funcional

El proyecto es una aplicación Django monolítica que sirve tanto el backend (API y lógica) como el frontend (a través de Django Templates).

### Características Principales

1.  **Múltiples Bases de Datos**: El sistema utiliza un `Database Router` para separar las tablas de autenticación/sesiones (`auth`, `admin`, etc.) de las tablas de negocio (`ventas`).
2.  **Integración API**: Contiene servicios para comunicarse con APIs externas (SII y Aula) para sincronizar datos de alumnos/clientes.
3.  **Gestión de Ventas**: Lógica completa para carrito de compras y registro de transacciones.

## Estructura de Carpetas

*   **`api/`**: Es el directorio de configuración del proyecto (lo que usualmente se llama `config` o el nombre del proyecto en Django). Contiene `settings.py`, `urls.py` principal y la configuración WSGI/ASGI.
    *   **`dbrouters/`**: Contiene la lógica para el enrutamiento de base de datos (`auth_router.py`).
*   **`ventas/`**: Es la "app" principal de Django que contiene la lógica de negocio.
    *   `models.py`: Definición de tablas (`Cliente`, `Producto`, `Venta`).
    *   `views.py`: Controladores de las vistas.
    *   `services.py`: Lógica de integración con servicios externos.
*   **`templates/`**: Archivos HTML para la interfaz de usuario.
*   **`static/`**: Archivos estáticos (CSS, imágenes, JS).
*   **`docs/`**: Documentación detallada del proyecto.

## Cómo levantar el proyecto

### Prerrequisitos

*   Python 3.8+
*   PostgreSQL
*   Virtualenv (recomendado)

### Pasos de Instalación

1.  **Clonar el repositorio y entrar a la carpeta**:
    ```bash
    cd ventas-django
    ```

2.  **Crear y activar un entorno virtual**:
    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate
    # En Linux/Mac
    source venv/bin/activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno**:
    Crea un archivo `.env` en la raíz de `ventas-django/` basándote en la configuración requerida en `api/settings.py`. Necesitarás configurar las bases de datos `default` y `auth`.

    Ejemplo básico:
    ```env
    DEBUG=True
    SECRET_KEY=tu_clave_secreta

    # Base de datos principal (Negocio)
    DB_NAME=ventas_db
    DB_USER=usuario
    DB_PASSWORD=password
    DB_HOST=localhost
    DB_PORT=5432

    # Base de datos de autenticación
    AUTH_NAME=auth_db
    AUTH_USER=usuario
    AUTH_PASSWORD=password
    AUTH_HOST=localhost
    AUTH_PORT=5432
    ```

5.  **Migraciones**:
    ```bash
    python manage.py migrate
    python manage.py migrate --database=auth
    ```

6.  **Crear Superusuario**:
    ```bash
    python manage.py createsuperuser --database=auth
    ```

7.  **Correr el servidor**:
    ```bash
    python manage.py runserver
    ```

Para más detalles, consulta la carpeta `docs/`.
