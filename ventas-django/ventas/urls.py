from django.urls import path

from . import views

urlpatterns = [
    path('carrito/', views.carrito_view, name='Carrito'),
    path('carrito', views.carrito_view),
    path('ventas/', views.ventas_view, name='Ventas'),
    path('clientes/', views.clientes_view, name='Clientes'),
    path('add_cliente/', views.add_clientes_view, name='AddCliente'),
    path('edit_cliente/', views.edit_clientes_view, name='EditCliente'),
    path('delete_cliente/', views.delete_clientes_view, name='DeleteCliente'),
    path('cursos/', views.cursos_view, name='Cursos'),
    path('add_curso/', views.add_curso_view, name='AddCurso'),
    path('delete_curso/', views.delete_curso_view, name='DeleteCurso'),
    path('edit_curso/', views.edit_curso_view, name='EditCurso'),
    path('inventario/', views.cursos_view, name='Inventario'),
    path('add_producto/', views.add_curso_view, name='AddProducto'),
    path('delete_producto/', views.delete_curso_view, name='DeleteProducto'),
    path('edit_producto/', views.edit_curso_view, name='EditProducto'),
    path('edit_venta/', views.edit_venta_view, name='EditVenta'),
    path('delete_venta/', views.delete_venta_view, name='DeleteVenta'),
    path('add_carrito/', views.add_carrito_view, name='AddCarrito'),
]
