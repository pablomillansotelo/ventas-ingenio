"""
Señales para sincronización con otros módulos
"""
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cliente, Inscripcion
from .services import buscar_alumno_por_email, crear_alumno_desde_cliente, registrar_inscripcion_aula

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Cliente)
def sincronizar_cliente_con_alumno(sender, instance, created, **kwargs):
    if not created:
        return

    alumno_existente = buscar_alumno_por_email(instance.email)
    if alumno_existente:
        alumno_id = alumno_existente.get('id') or alumno_existente.get('id_alumno')
        if alumno_id and not instance.id_alumno_sii:
            Cliente.objects.filter(pk=instance.pk).update(id_alumno_sii=alumno_id)
        logger.info('Alumno ya existe para cliente %s', instance.id_cliente)
        return

    resultado = crear_alumno_desde_cliente(instance)
    if not resultado:
        logger.warning('No se pudo sincronizar alumno para cliente %s', instance.id_cliente)


@receiver(post_save, sender=Inscripcion)
def sincronizar_inscripcion_aula(sender, instance, created, **kwargs):
    if created and instance.estado == Inscripcion.ESTADO_ACTIVA:
        registrar_inscripcion_aula(instance)
