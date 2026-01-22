# Guía de Instalación y Configuración

Esta guía detalla los pasos necesarios para configurar el entorno de desarrollo para **Ventas Ingenio**.

## Requisitos del Sistema

*   **Python**: Versión 3.8 o superior.
*   **PostgreSQL**: Base de datos relacional.
*   **Git**: Para control de versiones.

## Configuración de Base de Datos

El sistema requiere dos bases de datos lógicas (pueden residir en el mismo servidor PostgreSQL).

1.  **Base de Datos de Negocio (`default`)**: Almacenará clientes, productos y ventas.
2.  **Base de Datos de Autenticación (`auth`)**: Almacenará usuarios, sesiones y permisos.

Crea las bases de datos en tu servidor PostgreSQL:

```sql
CREATE DATABASE ventas_db;
CREATE DATABASE auth_db;
```

## Configuración del Entorno

1.  **Clonar el repositorio**:
    ```bash
    git clone <url-del-repo>
    cd ventas-ingenio/ventas-django
    ```

2.  **Entorno Virtual**:
    Es altamente recomendable usar un entorno virtual.
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    ```

3.  **Instalar Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Variables de Entorno (`.env`)**:
    Crea un archivo `.env` en la carpeta `ventas-django/`. Puedes copiar el siguiente contenido y ajustar los valores:

    ```ini
    # Configuración General
    DEBUG=True
    SECRET_KEY=django-insecure-tu-clave-secreta-aqui
    ALLOWED_HOSTS=127.0.0.1,localhost

    # Base de Datos PRINCIPAL (Negocio)
    DB_NAME=ventas_db
    DB_USER=postgres
    DB_PASSWORD=tu_password
    DB_HOST=localhost
    DB_PORT=5432

    # Base de Datos AUTH (Usuarios/Admin)
    AUTH_NAME=auth_db
    AUTH_USER=postgres
    AUTH_PASSWORD=tu_password
    AUTH_HOST=localhost
    AUTH_PORT=5432

    # Integraciones (Opcional para dev local)
    SII_API_URL=http://localhost:8001/api/alumnos/
    AULA_API_URL=http://localhost:8002/api/
    ```

## Inicialización de la Base de Datos

Dado que usamos múltiples bases de datos, debemos correr las migraciones para ambas.

1.  **Migrar base de datos principal (`default`)**:
    ```bash
    python manage.py migrate
    ```

2.  **Migrar base de datos de autenticación (`auth`)**:
    ```bash
    python manage.py migrate --database=auth
    ```

## Crear Usuario Administrador

El superusuario debe crearse en la base de datos `auth`.

```bash
python manage.py createsuperuser --database=auth
```

## Ejecutar el Servidor

```bash
python manage.py runserver
```

Accede a `http://127.0.0.1:8000/`.
