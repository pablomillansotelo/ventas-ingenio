from decimal import Decimal

from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)
    direccion = models.CharField(max_length=120, blank=True, default='')
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    curp = models.CharField(max_length=18, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    id_alumno_sii = models.IntegerField(blank=True, null=True)
    notas = models.TextField(blank=True, default='')
    activo = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'cat_cliente'

    def __str__(self):
        return f'{self.id_cliente} - {self.nombre} {self.apellidos}'

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellidos}'


class Vendedor(models.Model):
    id_vendedor = models.AutoField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=True, default='')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    comision_pct = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    activo = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'cat_vendedor'

    def __str__(self):
        return self.nombre

    @classmethod
    def obtener_o_crear_desde_usuario(cls, user):
        nombre = user.get_full_name().strip() or user.username
        vendedor, _ = cls.objects.get_or_create(
            user_id=user.id,
            defaults={
                'nombre': nombre,
                'email': user.email or '',
            },
        )
        return vendedor


class Curso(models.Model):
    MODALIDAD_PRESENCIAL = 'presencial'
    MODALIDAD_ONLINE = 'online'
    MODALIDAD_HIBRIDO = 'hibrido'
    MODALIDAD_CHOICES = [
        (MODALIDAD_PRESENCIAL, 'Presencial'),
        (MODALIDAD_ONLINE, 'En linea'),
        (MODALIDAD_HIBRIDO, 'Hibrido'),
    ]

    id_curso = models.AutoField(primary_key=True, db_column='id_producto')
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=120, db_column='producto')
    descripcion = models.TextField(blank=True, default='')
    duracion_horas = models.PositiveSmallIntegerField(blank=True, null=True)
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES, default=MODALIDAD_ONLINE)
    precio_lista = models.DecimalField(max_digits=19, decimal_places=4, db_column='precio_unitario')
    activo = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'cat_producto'

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class EdicionCurso(models.Model):
    ESTADO_PROGRAMADA = 'programada'
    ESTADO_EN_CURSO = 'en_curso'
    ESTADO_CERRADA = 'cerrada'
    ESTADO_CHOICES = [
        (ESTADO_PROGRAMADA, 'Programada'),
        (ESTADO_EN_CURSO, 'En curso'),
        (ESTADO_CERRADA, 'Cerrada'),
    ]

    id_edicion = models.AutoField(primary_key=True)
    id_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='id_curso', related_name='ediciones')
    codigo_edicion = models.CharField(max_length=30, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    cupo_maximo = models.PositiveSmallIntegerField(default=20)
    cupo_ocupado = models.PositiveSmallIntegerField(default=0)
    precio_edicion = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_PROGRAMADA)
    activo = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'cat_edicion_curso'

    def __str__(self):
        return f'{self.codigo_edicion} ({self.id_curso.codigo})'

    @property
    def cupo_disponible(self):
        return max(0, self.cupo_maximo - self.cupo_ocupado)

    @property
    def precio_aplicable(self):
        if self.precio_edicion is not None:
            return self.precio_edicion
        return self.id_curso.precio_lista

    def reservar_cupo(self, plazas=1):
        if self.cupo_disponible < plazas:
            raise ValueError('Cupo insuficiente en la edición')
        self.cupo_ocupado += plazas
        self.save(update_fields=['cupo_ocupado'])


class Venta(models.Model):
    ESTADO_CONFIRMADA = 'confirmada'
    ESTADO_CANCELADA = 'cancelada'
    ESTADO_CHOICES = [
        (ESTADO_CONFIRMADA, 'Confirmada'),
        (ESTADO_CANCELADA, 'Cancelada'),
    ]

    PAGO_PENDIENTE = 'pendiente'
    PAGO_PARCIAL = 'parcial'
    PAGO_PAGADO = 'pagado'
    ESTADO_PAGO_CHOICES = [
        (PAGO_PENDIENTE, 'Pendiente'),
        (PAGO_PARCIAL, 'Parcial'),
        (PAGO_PAGADO, 'Pagado'),
    ]

    id_venta = models.AutoField(primary_key=True)
    folio = models.CharField(max_length=20, unique=True, blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_vendedor = models.ForeignKey(
        Vendedor,
        models.DO_NOTHING,
        db_column='id_vendedor',
        blank=True,
        null=True,
        related_name='ventas',
    )
    fecha = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_CONFIRMADA)
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default=PAGO_PENDIENTE)
    observaciones = models.TextField(blank=True, default='')
    registrado_en = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        managed = True
        db_table = 'tra_venta'

    def __str__(self):
        return self.folio or str(self.id_venta)

    def save(self, *args, **kwargs):
        if not self.folio and self.pk is None:
            super().save(*args, **kwargs)
            self.folio = f'V-{self.pk:06d}'
            return super().save(update_fields=['folio'])
        return super().save(*args, **kwargs)

    @property
    def cliente(self):
        return self.id_cliente.nombre_completo

    @property
    def vendedor_nombre(self):
        return self.id_vendedor.nombre if self.id_vendedor_id else '—'

    @property
    def monto(self):
        total = Decimal('0')
        for detalle in self.ventadetalle_set.all():
            total += detalle.subtotal
        return total

    @property
    def total_pagado(self):
        total = self.pago_set.filter(estado=Pago.ESTADO_APLICADO).aggregate(
            total=models.Sum('monto')
        )['total']
        return total or Decimal('0')

    @property
    def saldo_pendiente(self):
        return max(Decimal('0'), self.monto - self.total_pagado)

    def actualizar_estado_pago(self):
        if self.total_pagado <= 0:
            self.estado_pago = self.PAGO_PENDIENTE
        elif self.total_pagado >= self.monto:
            self.estado_pago = self.PAGO_PAGADO
        else:
            self.estado_pago = self.PAGO_PARCIAL
        self.save(update_fields=['estado_pago'])


class VentaDetalle(models.Model):
    id_venta_det = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, models.DO_NOTHING, db_column='id_venta')
    id_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='id_producto')
    id_edicion = models.ForeignKey(
        EdicionCurso,
        models.DO_NOTHING,
        db_column='id_edicion',
        blank=True,
        null=True,
        related_name='ventas_detalle',
    )
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    descuento = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tra_venta_det'
        unique_together = (('id_venta', 'id_curso', 'id_edicion'),)

    @property
    def precio_aplicado(self):
        if self.precio_unitario is not None:
            return self.precio_unitario
        if self.id_edicion_id:
            return self.id_edicion.precio_aplicable
        return self.id_curso.precio_lista

    @property
    def subtotal(self):
        bruto = Decimal(self.cantidad) * self.precio_aplicado
        descuento = self.descuento or Decimal('0')
        return bruto - descuento


class Pago(models.Model):
    METODO_EFECTIVO = 'efectivo'
    METODO_TRANSFERENCIA = 'transferencia'
    METODO_TARJETA = 'tarjeta'
    METODO_CREDITO = 'credito'
    METODO_CHOICES = [
        (METODO_EFECTIVO, 'Efectivo'),
        (METODO_TRANSFERENCIA, 'Transferencia'),
        (METODO_TARJETA, 'Tarjeta'),
        (METODO_CREDITO, 'Crédito'),
    ]

    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_APLICADO = 'aplicado'
    ESTADO_RECHAZADO = 'rechazado'
    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_APLICADO, 'Aplicado'),
        (ESTADO_RECHAZADO, 'Rechazado'),
    ]

    id_pago = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, models.DO_NOTHING, db_column='id_venta', related_name='pago_set')
    monto = models.DecimalField(max_digits=19, decimal_places=4)
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES, default=METODO_TRANSFERENCIA)
    referencia = models.CharField(max_length=60, blank=True, default='')
    fecha_pago = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_APLICADO)

    class Meta:
        managed = True
        db_table = 'tra_pago'

    def __str__(self):
        return f'Pago #{self.id_pago} — ${self.monto}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.estado == self.ESTADO_APLICADO:
            self.id_venta.actualizar_estado_pago()


class Inscripcion(models.Model):
    ESTADO_ACTIVA = 'activa'
    ESTADO_CANCELADA = 'cancelada'
    ESTADO_COMPLETADA = 'completada'
    ESTADO_CHOICES = [
        (ESTADO_ACTIVA, 'Activa'),
        (ESTADO_CANCELADA, 'Cancelada'),
        (ESTADO_COMPLETADA, 'Completada'),
    ]

    id_inscripcion = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente', related_name='inscripciones')
    id_edicion = models.ForeignKey(
        EdicionCurso,
        models.DO_NOTHING,
        db_column='id_edicion',
        blank=True,
        null=True,
        related_name='inscripciones',
    )
    id_curso = models.ForeignKey(
        Curso,
        models.DO_NOTHING,
        db_column='id_curso',
        related_name='inscripciones',
    )
    id_venta_det = models.ForeignKey(
        VentaDetalle,
        models.DO_NOTHING,
        db_column='id_venta_det',
        blank=True,
        null=True,
        related_name='inscripciones',
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=ESTADO_ACTIVA)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    id_alumno_externo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tra_inscripcion'

    def __str__(self):
        curso = self.id_edicion.codigo_edicion if self.id_edicion_id else self.id_curso.codigo
        return f'{self.id_cliente.nombre_completo} → {curso}'


# Alias temporal para compatibilidad con imports legacy
Producto = Curso
