from django.db import models

# Create your models here.

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)
    direccion = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cat_cliente'

    def __str__(self):
        return str(self.id_cliente) + ' - ' + self.nombre + ' ' +self.apellidos

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    producto = models.CharField(max_length=40)
    precio_unitario = models.DecimalField(max_digits=19, decimal_places=4)

    class Meta:
        managed = True
        db_table = 'cat_producto'

    def __str__(self):
        return str(self.id_producto) + ' - ' +self.producto


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tra_venta'

    def __str__(self):
        return str(self.id_venta)

class VentaDetalle(models.Model):
    id_venta_det = models.AutoField(primary_key=True)  
    id_venta = models.ForeignKey(Venta, models.DO_NOTHING, db_column='id_venta')
    id_producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='id_producto')
    cantidad = models.IntegerField()
    descuento = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tra_venta_det'
        unique_together = (('id_venta', 'id_producto'),)



