"""
Servicios para integración con otros módulos
"""
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def crear_alumno_desde_cliente(cliente):
    """
    Crea un alumno en SII cuando se crea un cliente en Ventas.
    
    Args:
        cliente: Instancia del modelo Cliente
        
    Returns:
        dict: Respuesta de la API o None si hay error
    """
    # URL de la API de SII (debe configurarse en settings)
    sii_api_url = getattr(settings, 'SII_API_URL', 'http://localhost:8000/api/alumnos/')
    
    # Datos del alumno basados en el cliente
    datos_alumno = {
        'nombre': cliente.nombre,
        'apellido': cliente.apellidos,
        'email': cliente.email,
        'curp': '',  # No disponible en cliente, se puede actualizar después
        'fecha_nacimiento': '2000-01-01',  # Valor por defecto
        'estado': 'activo'
    }
    
    try:
        response = requests.post(
            sii_api_url,
            json=datos_alumno,
            timeout=5
        )
        
        if response.status_code in [200, 201]:
            logger.info(f"Alumno creado exitosamente para cliente {cliente.id_cliente}")
            return response.json()
        else:
            logger.error(f"Error al crear alumno: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión al crear alumno: {str(e)}")
        return None


def buscar_alumno_por_email(email):
    """
    Busca un alumno en SII por email.
    
    Args:
        email: Email del alumno a buscar
        
    Returns:
        dict: Datos del alumno o None si no se encuentra
    """
    sii_api_url = getattr(settings, 'SII_API_URL', 'http://localhost:8000/api/alumnos/')
    buscar_url = f"{sii_api_url}buscar_por_email/?email={email}"
    
    try:
        response = requests.get(buscar_url, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            logger.error(f"Error al buscar alumno: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión al buscar alumno: {str(e)}")
        return None

