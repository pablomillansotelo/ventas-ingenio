from django.shortcuts import render, redirect
from .models import Cliente, Producto
from .forms import AddClienteForm, EditarClienteForm, AddProductoForm, EditarProductoForm, EditarVentaForm, AddVentaForm, AddVentaDetalleForm
from django.contrib import messages
from django import forms
from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def carrito_view(request):
    cursor = connections['default'].cursor()
    productos = Producto.objects.all()
    form_venta = AddVentaForm
    form_add_venta_detalle = AddVentaDetalleForm

    context = {
        'form_venta': form_venta,
        'form_add_venta_detalle': form_add_venta_detalle,
        #'form_editar_venta': form_editar_venta,
    }
    return render(request, 'carrito.html', context)

@login_required
@csrf_exempt
def add_carrito_view(request):
    cursor = connections['default'].cursor()
    productos = Producto.objects.all()
    if request.method == "POST":
        nplainArray = request.POST.getlist('nplainArray[]')
        id_cliente_add = request.POST.get('id_cliente_add')
        fecha_add = request.POST.get('fecha_add')
        print('Agregar cliente: ' + id_cliente_add)
        print('Agregar fecha: ' + fecha_add)
        print('id del producto 0: ' + request.POST.get('nplainArray[0]'))
        #print('id del producto 0: ' + request.POST.get('nplainArray[0][1]'))
        #print('id del producto 0: ' + request.POST.get('nplainArray[0][2]'))
        #print('id del producto 0: ' + nplainArray[0][3])
        #print('id del producto 1' + nplainArray[1][0])
        #cursor.execute("declare @tabla_temp as venta_detalleTableType")
        #cursor.execute("insert into @tabla_temp (id_producto_tt, cantidad_tt, descuento_tt) values ("+nplainArray[0].id_producto +", "+ nplainArray[0].cantidad +")")
        messages.success(request, "Column data are updated successfully!")

    return redirect('Carrito')

@login_required
def ventas_view(request):
    cursor = connections['default'].cursor()
    ventas = cursor.execute('EXEC mostrar_ventas')
    form_editar_venta = EditarVentaForm
    context = {
        'Ventas': ventas,
        'form_editar_venta': form_editar_venta,
    }
    return render(request, 'ventas.html', context)

@login_required
def edit_venta_view(request):
    if request.POST.get('nombre') and request.POST.get('apellidos') and request.POST.get(
            'direccion') and request.POST.get('email') and request.POST.get('telefono'):
        cliente_temporal = Cliente()
        cliente_temporal.id_cliente = request.POST.get('id_personal_editar')
        cliente_temporal.nombre = request.POST.get('nombre')
        cliente_temporal.apellidos = request.POST.get('apellidos')
        cliente_temporal.direccion = request.POST.get('direccion')
        cliente_temporal.email = request.POST.get('email')
        cliente_temporal.telefono = request.POST.get('telefono')
        cursor = connections['default'].cursor()
        cursor.execute("EXEC modificar_cliente " + cliente_temporal.id_cliente + ", '"+ cliente_temporal.nombre + "', '"+ cliente_temporal.apellidos + "', '"+ cliente_temporal.direccion + "', '" + cliente_temporal.email + "', '" + cliente_temporal.telefono + "'")
        messages.success(request, 'El cliente ha sido modificado')
    return redirect('Ventas')

@login_required
def clientes_view(request):
    clientes = Cliente.objects.all()
    form_cliente = AddClienteForm
    form_editar_cliente = EditarClienteForm
    context = {
        'Clientes': clientes,
        'form_cliente': form_cliente,
        'form_editar_cliente': form_editar_cliente,
    }
    return render(request, 'clientes.html', context)

@login_required
def add_clientes_view(request):
    if request.POST:
        if request.POST.get('nombre') and request.POST.get('apellidos') and request.POST.get(
                'direccion') and request.POST.get('email') and request.POST.get('telefono'):
            cliente_temporal = Cliente()
            cliente_temporal.nombre = request.POST.get('nombre')
            cliente_temporal.apellidos = request.POST.get('apellidos')
            cliente_temporal.direccion = request.POST.get('direccion')
            cliente_temporal.email = request.POST.get('email')
            cliente_temporal.telefono = request.POST.get('telefono')
            cursor = connections['default'].cursor()
            cursor.execute(
                "EXEC insertar_cliente '" + cliente_temporal.nombre + "', '" + cliente_temporal.apellidos + "', '" + cliente_temporal.direccion + "', '" + cliente_temporal.email + "', '" + cliente_temporal.telefono + "'")
            messages.success(request, 'El cliente ha sido agregado')
    return redirect('Clientes')

@login_required
def edit_clientes_view(request):
    if request.POST.get('nombre') and request.POST.get('apellidos') and request.POST.get(
            'direccion') and request.POST.get('email') and request.POST.get('telefono'):
        cliente_temporal = Cliente()
        cliente_temporal.id_cliente = request.POST.get('id_personal_editar')
        cliente_temporal.nombre = request.POST.get('nombre')
        cliente_temporal.apellidos = request.POST.get('apellidos')
        cliente_temporal.direccion = request.POST.get('direccion')
        cliente_temporal.email = request.POST.get('email')
        cliente_temporal.telefono = request.POST.get('telefono')
        cursor = connections['default'].cursor()
        cursor.execute("EXEC modificar_cliente " + cliente_temporal.id_cliente + ", '"+ cliente_temporal.nombre + "', '"+ cliente_temporal.apellidos + "', '"+ cliente_temporal.direccion + "', '" + cliente_temporal.email + "', '" + cliente_temporal.telefono + "'")
        messages.success(request, 'El cliente ha sido modificado')
    return redirect('Clientes')

@login_required
def delete_clientes_view(request):
    if request.POST:
        cursor = connections['default'].cursor()
        print("El id a eliminar: " + request.POST.get('id_personal_eliminar'))
        cursor.execute("EXEC eliminar_cliente " + request.POST.get('id_personal_eliminar'))
        messages.success(request, 'El cliente ha sido eliminado')

    return redirect('Clientes')

@login_required
def inventario_view(request):
    productos = Producto.objects.all()
    form_producto = AddProductoForm
    form_editar_producto = EditarProductoForm
    context = {
        'Productos': productos,
        'form_producto': form_producto,
        'form_editar_producto': form_editar_producto,
    }
    return render(request, 'inventario.html', context)

@login_required
def add_producto_view(request):
    if request.POST:
        if request.POST.get('producto') and request.POST.get('precio_unitario') :
            producto_temporal = Producto()
            producto_temporal.producto = request.POST.get('producto')
            producto_temporal.precio_unitario = request.POST.get('precio_unitario')
            cursor = connections['default'].cursor()
            cursor.execute(
                "EXEC insertar_producto '" + producto_temporal.producto + "', " + producto_temporal.precio_unitario)
            messages.success(request, 'El producto ha sido agregado')
    return redirect('Inventario')

@login_required
def delete_producto_view(request):
    if request.POST:
        cursor = connections['default'].cursor()
        print("El id a eliminar: " + request.POST.get('id_producto_eliminar'))
        cursor.execute("EXEC eliminar_producto " + request.POST.get('id_producto_eliminar'))
        messages.success(request, 'El producto ha sido eliminado')
    return redirect('Inventario')

@login_required
def edit_producto_view(request):
    producto_temporal = Producto()
    producto_temporal.id_producto = request.POST.get('id_producto_editar')
    producto_temporal.producto = request.POST.get('producto')
    producto_temporal.precio_unitario = request.POST.get('precio_unitario')
    cursor = connections['default'].cursor()
    cursor.execute(
        "EXEC modificar_producto " + producto_temporal.id_producto + ", '" + producto_temporal.producto + "', " + producto_temporal.precio_unitario)
    messages.success(request, 'El producto ha sido modificado')
    return redirect('Inventario')

@login_required
def delete_venta_view(request):
    if request.POST:
        cursor = connections['default'].cursor()
        print("El id a eliminar: " + request.POST.get('id_venta_eliminar'))
        cursor.execute("EXEC eliminar_venta " + request.POST.get('id_venta_eliminar'))
        messages.success(request, 'La venta y su contenido se ha eliminado')

    return redirect('Clientes')