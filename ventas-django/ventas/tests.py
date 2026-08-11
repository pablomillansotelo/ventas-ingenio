from decimal import Decimal
from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from .models import Cliente, Producto, Venta, VentaDetalle


class VentaModelTests(TestCase):
    databases = {'default'}

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Ana',
            apellidos='Garcia',
            direccion='Calle 1',
            email='ana@test.com',
            telefono='5551234',
        )
        self.producto = Producto.objects.create(
            producto='Curso Python',
            precio_unitario=Decimal('100.0000'),
        )
        self.venta = Venta.objects.create(
            id_cliente=self.cliente,
            fecha=date(2025, 8, 1),
        )
        VentaDetalle.objects.create(
            id_venta=self.venta,
            id_producto=self.producto,
            cantidad=2,
            descuento=Decimal('10.0000'),
        )

    def test_cliente_property(self):
        self.assertEqual(self.venta.cliente, 'Ana Garcia')

    def test_monto_property(self):
        # (2 * 100) - 10 = 190
        self.assertEqual(self.venta.monto, Decimal('190.0000'))

    def test_monto_sin_descuento(self):
        venta = Venta.objects.create(id_cliente=self.cliente, fecha=date.today())
        VentaDetalle.objects.create(
            id_venta=venta,
            id_producto=self.producto,
            cantidad=1,
            descuento=None,
        )
        self.assertEqual(venta.monto, Decimal('100.0000'))


class VentaViewTests(TestCase):
    databases = {'default', 'auth'}

    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.http = Client()
        self.http.login(username='tester', password='secret123')

        self.cliente_a = Cliente.objects.create(
            nombre='Luis',
            apellidos='Perez',
            direccion='Calle 2',
            email='luis@test.com',
            telefono='5550000',
        )
        self.cliente_b = Cliente.objects.create(
            nombre='Maria',
            apellidos='Lopez',
            direccion='Calle 3',
            email='maria@test.com',
            telefono='5551111',
        )
        self.venta = Venta.objects.create(
            id_cliente=self.cliente_a,
            fecha=date(2025, 7, 15),
        )

    def test_edit_venta_view_actualiza_cliente_y_fecha(self):
        response = self.http.post(
            reverse('EditVenta'),
            {
                'id_venta_editar': self.venta.id_venta,
                'id_cliente': self.cliente_b.id_cliente,
                'fecha': '2025-08-10',
            },
        )
        self.assertRedirects(response, reverse('Ventas'))
        self.venta.refresh_from_db()
        self.assertEqual(self.venta.id_cliente_id, self.cliente_b.id_cliente)
        self.assertEqual(str(self.venta.fecha), '2025-08-10')

    def test_delete_venta_view_elimina_venta_y_detalles(self):
        producto = Producto.objects.create(producto='Libro', precio_unitario=Decimal('50'))
        VentaDetalle.objects.create(
            id_venta=self.venta,
            id_producto=producto,
            cantidad=1,
        )
        response = self.http.post(
            reverse('DeleteVenta'),
            {'id_venta_eliminar': self.venta.id_venta},
        )
        self.assertRedirects(response, reverse('Ventas'))
        self.assertFalse(Venta.objects.filter(pk=self.venta.id_venta).exists())
        self.assertFalse(VentaDetalle.objects.filter(id_venta=self.venta.id_venta).exists())

    def test_delete_venta_url_usa_vista_correcta(self):
        from ventas import urls as ventas_urls

        delete_pattern = next(p for p in ventas_urls.urlpatterns if p.name == 'DeleteVenta')
        self.assertEqual(delete_pattern.callback.__name__, 'delete_venta_view')
