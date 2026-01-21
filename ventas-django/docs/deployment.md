# Despliegue

## Vercel

El proyecto contiene un archivo de configuración `vercel.json` en la raíz de `ventas-django`, lo que indica que está preparado para ser desplegado en la plataforma **Vercel** como una aplicación Serverless.

### Configuración `vercel.json`

```json
{
  "builds": [
    {
      "src": "api/wsgi.py",
      "use": "@vercel/python",
      "config": { "maxLambdaSize": "15mb", "runtime": "python3.9" }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/wsgi.py"
    }
  ]
}
```

Esta configuración apunta a `api/wsgi.py` como punto de entrada de la aplicación.

### Consideraciones para Producción

1.  **Archivos Estáticos**:
    Se utiliza `whitenoise` para servir archivos estáticos eficientemente en producción, ya que Vercel (y otros entornos serverless) no persisten el sistema de archivos de la misma manera que un servidor tradicional.

    En `settings.py`:
    ```python
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    ```

2.  **Base de Datos**:
    En producción, asegúrate de que las variables de entorno (`DB_HOST`, etc.) apunten a una instancia de base de datos PostgreSQL accesible desde internet (por ejemplo, AWS RDS, Supabase, Neon, etc.).

3.  **Variables de Entorno**:
    Configura todas las variables definidas en `.env` dentro del panel de configuración de Vercel.

    *   `SECRET_KEY`
    *   `DEBUG` (Debe ser `False`)
    *   Variables de DB (`DB_NAME`, `DB_HOST`...)
    *   Variables de Auth DB (`AUTH_NAME`, `AUTH_HOST`...)
