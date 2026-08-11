from django.contrib import admin

from .models import Cliente, Curso, Vendedor, Venta, VentaDetalle

admin.site.register(Cliente)
admin.site.register(Curso)
admin.site.register(Vendedor)
admin.site.register(Venta)
admin.site.register(VentaDetalle)
