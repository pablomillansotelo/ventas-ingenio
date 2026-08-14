# Ventas Ingenio

Sistema de **venta e inscripción de cursos** para Modelo Ingenio. Monolito Django con UI sidebar, catálogos, punto de venta, pagos e integración con SII/Aula.

## Funcionalidades

- **Panel de control** — KPIs de ventas, inscripciones y cobros pendientes
- **Punto de venta** — Carrito multi-curso con ediciones (cohortes) y cupo
- **Ventas** — Historial con folio, detalle, estado de venta y pago
- **Pagos** — Registro de cobros (efectivo, transferencia, tarjeta, crédito)
- **Inscripciones** — Matrículas vinculadas a ventas y ediciones
- **Catálogos** — Clientes, vendedores, cursos y ediciones
- **Integración** — Sync automático de alumnos (SII) e inscripciones (Aula)

## Stack

- Django 4.2 + PostgreSQL (dual DB: negocio + auth)
- Bootstrap 5 + design tokens
- Deploy en Vercel + Neon Postgres

## Estructura

- `ventas-django/` — Aplicación Django
- `ventas-sql/init.sql` — Esquema canónico PostgreSQL

## Documentación

Ver `ventas-django/docs/architecture.md` para el modelo de datos, rutas y flujos.
