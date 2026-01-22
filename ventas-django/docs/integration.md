# Integración con Sistemas Externos

El módulo de ventas no funciona de manera aislada; está diseñado para integrarse con otros sistemas institucionales, específicamente un Sistema Integral de Información (SII) y un sistema de Aula.

## Servicios de Integración (`ventas/services.py`)

La lógica de integración se encuentra encapsulada en `ventas/services.py`.

### 1. Creación de Alumnos (SII API)

Cuando se registra un nuevo cliente en el sistema de ventas, el sistema intenta automáticamente registrar a ese cliente como un "Alumno" en el sistema SII.

*   **Trigger**: Creación de un `Cliente`.
*   **Endpoint**: `POST /api/alumnos/` (Configurable vía `SII_API_URL`).
*   **Datos enviados**:
    *   `nombre`
    *   `apellido`
    *   `email`
    *   `fecha_nacimiento` (default: '2000-01-01')
    *   `estado`: 'activo'

### 2. Búsqueda de Alumnos

Existe funcionalidad para buscar si un alumno ya existe en el sistema externo mediante su correo electrónico.

*   **Endpoint**: `GET /api/alumnos/buscar_por_email/?email={email}`

## Configuración

Las URLs de las APIs externas se configuran a través de variables de entorno en `settings.py`:

```python
SII_API_URL = config('SII_API_URL', default='http://localhost:8001/api/alumnos/')
AULA_API_URL = config('AULA_API_URL', default='http://localhost:8002/api/')
```

### Manejo de Errores

Las integraciones están diseñadas para ser resilientes. Si la API externa no está disponible o devuelve un error, el sistema de ventas registra el error en los logs (`logger.error`) pero no necesariamente interrumpe el flujo principal de venta, aunque la sincronización no se haya completado.
