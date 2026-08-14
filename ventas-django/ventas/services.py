"""
Servicios para integración con otros módulos
"""
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def crear_alumno_desde_cliente(cliente):
    """
    Crea un alumno en SII cuando se crea un cliente en Ventas.
    """
    sii_api_url = getattr(settings, 'SII_API_URL', 'http://localhost:8000/api/alumnos/')

    datos_alumno = {
        'nombre': cliente.nombre,
        'apellido': cliente.apellidos,
        'email': cliente.email,
        'curp': cliente.curp or '',
        'fecha_nacimiento': '2000-01-01',
        'estado': 'activo',
    }

    try:
        response = requests.post(sii_api_url, json=datos_alumno, timeout=5)
        if response.status_code in [200, 201]:
            data = response.json()
            alumno_id = data.get('id') or data.get('id_alumno')
            if alumno_id and not cliente.id_alumno_sii:
                cliente.id_alumno_sii = alumno_id
                cliente.save(update_fields=['id_alumno_sii'])
            logger.info('Alumno creado para cliente %s', cliente.id_cliente)
            return data
        logger.error('Error al crear alumno: %s - %s', response.status_code, response.text)
        return None
    except requests.exceptions.RequestException as exc:
        logger.error('Error de conexión al crear alumno: %s', exc)
        return None


def buscar_alumno_por_email(email):
    sii_api_url = getattr(settings, 'SII_API_URL', 'http://localhost:8000/api/alumnos/')
    buscar_url = f'{sii_api_url}buscar_por_email/?email={email}'

    try:
        response = requests.get(buscar_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 404:
            return None
        logger.error('Error al buscar alumno: %s', response.status_code)
        return None
    except requests.exceptions.RequestException as exc:
        logger.error('Error de conexión al buscar alumno: %s', exc)
        return None


def registrar_inscripcion_aula(inscripcion):
    """Notifica inscripción al módulo Aula (best-effort)."""
    aula_api_url = getattr(settings, 'AULA_API_URL', 'http://localhost:8002/api/')
    url = f'{aula_api_url}inscripciones/'

    payload = {
        'cliente_id': inscripcion.id_cliente_id,
        'curso_id': inscripcion.id_curso_id,
        'edicion_id': inscripcion.id_edicion_id,
        'alumno_sii_id': inscripcion.id_cliente.id_alumno_sii,
        'estado': inscripcion.estado,
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code in [200, 201]:
            data = response.json()
            externo_id = data.get('id') or data.get('id_inscripcion')
            if externo_id:
                inscripcion.id_alumno_externo = externo_id
                inscripcion.save(update_fields=['id_alumno_externo'])
            return data
        logger.warning('Aula rechazó inscripción %s: %s', inscripcion.id_inscripcion, response.text)
        return None
    except requests.exceptions.RequestException as exc:
        logger.warning('No se pudo registrar inscripción en Aula: %s', exc)
        return None
