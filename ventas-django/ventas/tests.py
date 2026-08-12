from decimal import Decimal
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import (
    Cliente,
    Curso,
    EdicionCurso,
    Inscripcion,
    Pago,
    Vendedor,
    Venta,
    VentaDetalle,
)


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
        self.vendedor = Vendedor.objects.create(user_id=99, nombre='Carlos Vendedor', email='carlos@test.com')
        self.curso = Curso.objects.create(
            codigo='PY-101',
            nombre='Curso Python',
            precio_lista=Decimal('100.0000'),
        )
        self.venta = Venta.objects.create(
            id_cliente=self.cliente,
            id_vendedor=self.vendedor,
            fecha=date(2025, 8, 1),
        )
        VentaDetalle.objects.create(
            id_venta=self.venta,
            id_curso=self.curso,
            cantidad=2,
            precio_unitario=Decimal('100.0000'),
            descuento=Decimal('10.0000'),
        )

    def test_cliente_property(self):
        self.assertEqual(self.venta.cliente, 'Ana Garcia')

    def test_monto_property(self):
        self.assertEqual(self.venta.monto, Decimal('190.0000'))

    def test_folio_generado(self):
        self.assertTrue(self.venta.folio.startswith('V-'))

    def test_estado_pago_con_pago_parcial(self):
        Pago.objects.create(
            id_venta=self.venta,
            monto=Decimal('50.0000'),
            metodo=Pago.METODO_EFECTIVO,
        )
        self.venta.refresh_from_db()
        self.assertEqual(self.venta.estado_pago, Venta.PAGO_PARCIAL)
        self.assertEqual(self.venta.saldo_pendiente, Decimal('140.0000'))


class EdicionCursoTests(TestCase):
    databases = {'default'}

    def setUp(self):
        self.curso = Curso.objects.create(codigo='DJ-01', nombre='Django', precio_lista=Decimal('200'))
        self.edicion = EdicionCurso.objects.create(
            id_curso=self.curso,
            codigo_edicion='DJ-01-2026-01',
            fecha_inicio=date.today() + timedelta(days=7),
            cupo_maximo=10,
        )

    def test_reservar_cupo(self):
        self.edicion.reservar_cupo(2)
        self.edicion.refresh_from_db()
        self.assertEqual(self.edicion.cupo_ocupado, 2)
        self.assertEqual(self.edicion.cupo_disponible, 8)


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
        self.vendedor = Vendedor.objects.create(user_id=self.user.id, nombre='Tester', email='tester@test.com')
        self.venta = Venta.objects.create(
            id_cliente=self.cliente_a,
            id_vendedor=self.vendedor,
            fecha=date(2025, 7, 15),
        )

    def test_dashboard_view(self):
        response = self.http.get(reverse('Dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_edit_venta_view_actualiza_cliente_y_fecha(self):
        response = self.http.post(
            reverse('EditVenta'),
            {
                'id_venta_editar': self.venta.id_venta,
                'id_cliente': self.cliente_b.id_cliente,
                'fecha': '2025-08-10',
                'estado': 'confirmada',
                'estado_pago': 'pendiente',
                'observaciones': 'Nota test',
            },
        )
        self.assertRedirects(response, reverse('Ventas'))
        self.venta.refresh_from_db()
        self.assertEqual(self.venta.id_cliente_id, self.cliente_b.id_cliente)
        self.assertEqual(str(self.venta.fecha), '2025-08-10')

    def test_add_carrito_asigna_vendedor_y_crea_inscripcion(self):
        curso = Curso.objects.create(codigo='DJ-01', nombre='Django', precio_lista=Decimal('200'))
        response = self.http.post(
            reverse('AddCarrito'),
            {
                'id_cliente_add': self.cliente_a.id_cliente,
                'fecha_add': '2025-08-11',
                'observaciones_add': '',
                'nplainArray[]': f'{curso.id_curso},,1,0',
            },
        )
        self.assertRedirects(response, reverse('Ventas'))
        venta = Venta.objects.latest('id_venta')
        self.assertEqual(venta.id_vendedor.user_id, self.user.id)
        self.assertTrue(Inscripcion.objects.filter(id_venta_det__id_venta=venta).exists())

    def test_add_carrito_con_edicion(self):
        curso = Curso.objects.create(codigo='UX-01', nombre='UX', precio_lista=Decimal('150'))
        edicion = EdicionCurso.objects.create(
            id_curso=curso,
            codigo_edicion='UX-01-2026',
            fecha_inicio=date.today(),
            cupo_maximo=5,
        )
        response = self.http.post(
            reverse('AddCarrito'),
            {
                'id_cliente_add': self.cliente_a.id_cliente,
                'fecha_add': '2025-08-11',
                'nplainArray[]': f'{curso.id_curso},{edicion.id_edicion},1,0',
            },
        )
        self.assertRedirects(response, reverse('Ventas'))
        edicion.refresh_from_db()
        self.assertEqual(edicion.cupo_ocupado, 1)

    def test_pagos_view(self):
        response = self.http.get(reverse('Pagos'))
        self.assertEqual(response.status_code, 200)

    def test_delete_venta_view_elimina_venta_y_detalles(self):
        curso = Curso.objects.create(codigo='BK-01', nombre='Libro', precio_lista=Decimal('50'))
        VentaDetalle.objects.create(
            id_venta=self.venta,
            id_curso=curso,
            cantidad=1,
            precio_unitario=Decimal('50'),
        )
        response = self.http.post(
            reverse('DeleteVenta'),
            {'id_venta_eliminar': self.venta.id_venta},
        )
        self.assertRedirects(response, reverse('Ventas'))
        self.assertFalse(Venta.objects.filter(pk=self.venta.id_venta).exists())
