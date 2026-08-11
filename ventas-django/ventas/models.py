from decimal import Decimal

from django.db import models


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)
    direccion = models.CharField(max_length=120, blank=True, default='')
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    curp = models.CharField(max_length=18, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)

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


class Venta(models.Model):
    ESTADO_CONFIRMADA = 'confirmada'
    ESTADO_CANCELADA = 'cancelada'
    ESTADO_CHOICES = [
        (ESTADO_CONFIRMADA, 'Confirmada'),
        (ESTADO_CANCELADA, 'Cancelada'),
    ]

    id_venta = models.AutoField(primary_key=True)
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
    observaciones = models.TextField(blank=True, default='')
    registrado_en = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        managed = True
        db_table = 'tra_venta'

    def __str__(self):
        return str(self.id_venta)

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


class VentaDetalle(models.Model):
    id_venta_det = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(Venta, models.DO_NOTHING, db_column='id_venta')
    id_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='id_producto')
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    descuento = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tra_venta_det'
        unique_together = (('id_venta', 'id_curso'),)

    @property
    def precio_aplicado(self):
        if self.precio_unitario is not None:
            return self.precio_unitario
        return self.id_curso.precio_lista

    @property
    def subtotal(self):
        bruto = Decimal(self.cantidad) * self.precio_aplicado
        descuento = self.descuento or Decimal('0')
        return bruto - descuento


# Alias temporal para compatibilidad con imports legacy
Producto = Curso
