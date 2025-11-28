"""
Señales para sincronización con otros módulos
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cliente
from .services import crear_alumno_desde_cliente, buscar_alumno_por_email
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Cliente)
def sincronizar_cliente_con_alumno(sender, instance, created, **kwargs):
    """
    Señal que se dispara cuando se crea o actualiza un Cliente.
    Si es nuevo, intenta crear un Alumno en SII.
    """
    if created:
        # Verificar si ya existe un alumno con este email
        alumno_existente = buscar_alumno_por_email(instance.email)
        
        if not alumno_existente:
            # Crear nuevo alumno en SII
            resultado = crear_alumno_desde_cliente(instance)
            if resultado:
                logger.info(f"Alumno sincronizado para cliente {instance.id_cliente}")
            else:
                logger.warning(f"No se pudo sincronizar alumno para cliente {instance.id_cliente}")
        else:
            logger.info(f"Alumno ya existe para cliente {instance.id_cliente}")

