from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='ventas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('carrito/', views.carrito_view, name='Carrito'),
    path('carrito', views.carrito_view, name='Carrito'),
    path('ventas/', views.ventas_view, name='Ventas'),
    path('clientes/', views.clientes_view, name='Clientes'),
    path('add_cliente/', views.add_clientes_view, name='AddCliente'),
    path('edit_cliente/', views.edit_clientes_view, name='EditCliente'),
    path('delete_cliente/', views.delete_clientes_view, name='DeleteCliente'),
    path('inventario/', views.inventario_view, name='Inventario'),
    path('add_producto/', views.add_producto_view, name='AddProducto'),
    path('delete_producto/', views.delete_producto_view, name='DeleteProducto'),
    path('edit_producto/', views.edit_producto_view, name='EditProducto'),
    path('edit_venta/', views.edit_venta_view, name='EditVenta'),
    path('delete_venta/', views.edit_venta_view, name='DeleteVenta'),
    path('add_carrito/', views.add_carrito_view, name='AddCarrito'),
]