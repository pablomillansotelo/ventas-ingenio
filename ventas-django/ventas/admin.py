from django.contrib import admin

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

admin.site.register(Cliente)
admin.site.register(Curso)
admin.site.register(EdicionCurso)
admin.site.register(Vendedor)
admin.site.register(Venta)
admin.site.register(VentaDetalle)
admin.site.register(Pago)
admin.site.register(Inscripcion)
