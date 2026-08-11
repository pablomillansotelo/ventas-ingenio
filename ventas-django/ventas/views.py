from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import (
    AddClienteForm,
    AddCursoForm,
    AddVentaDetalleForm,
    AddVentaForm,
    EditarClienteForm,
    EditarCursoForm,
    EditarVentaForm,
)
from .models import Cliente, Curso, Vendedor, Venta, VentaDetalle


def _vendedor_actual(request):
    return Vendedor.obtener_o_crear_desde_usuario(request.user)


@login_required
def carrito_view(request):
    vendedor = _vendedor_actual(request)
    context = {
        'form_venta': AddVentaForm(),
        'form_add_venta_detalle': AddVentaDetalleForm(),
        'vendedor': vendedor,
    }
    return render(request, 'ventas/carrito.html', context)


@login_required
def add_carrito_view(request):
    if request.method != 'POST':
        return redirect('Carrito')

    id_cliente_add = request.POST.get('id_cliente_add')
    fecha_add = request.POST.get('fecha_add')
    observaciones = request.POST.get('observaciones_add', '')
    nplainArray = request.POST.getlist('nplainArray[]')

    try:
        cliente = Cliente.objects.get(pk=id_cliente_add)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente no encontrado')
        return redirect('Carrito')

    if not nplainArray:
        messages.error(request, 'Agrega al menos un curso al carrito')
        return redirect('Carrito')

    vendedor = _vendedor_actual(request)

    try:
        with transaction.atomic():
            venta = Venta.objects.create(
                id_cliente=cliente,
                id_vendedor=vendedor,
                fecha=fecha_add,
                observaciones=observaciones,
            )

            for item in nplainArray:
                partes = item.split(',')
                id_curso = partes[0]
                cantidad = partes[1]
                descuento = partes[2] if len(partes) > 2 and partes[2] else None

                curso = Curso.objects.get(pk=id_curso, activo=True)
                VentaDetalle.objects.create(
                    id_venta=venta,
                    id_curso=curso,
                    cantidad=cantidad,
                    precio_unitario=curso.precio_lista,
                    descuento=descuento or None,
                )
    except Curso.DoesNotExist:
        messages.error(request, 'Uno de los cursos seleccionados no esta disponible')
        return redirect('Carrito')
    except Exception:
        messages.error(request, 'No se pudo registrar la venta')
        return redirect('Carrito')

    messages.success(request, f'Venta #{venta.id_venta} registrada correctamente')
    return redirect('Ventas')


@login_required
def ventas_view(request):
    ventas = Venta.objects.select_related('id_cliente', 'id_vendedor').prefetch_related(
        'ventadetalle_set__id_curso'
    ).order_by('-fecha', '-id_venta')
    context = {
        'Ventas': ventas,
        'form_editar_venta': EditarVentaForm(),
    }
    return render(request, 'ventas/ventas.html', context)


@login_required
def edit_venta_view(request):
    if request.method == 'POST':
        venta_id = request.POST.get('id_venta_editar') or request.POST.get('id_venta')
        if not venta_id:
            messages.error(request, 'Venta no especificada')
            return redirect('Ventas')

        try:
            venta = Venta.objects.get(pk=venta_id)
        except Venta.DoesNotExist:
            messages.error(request, 'Venta no encontrada')
            return redirect('Ventas')

        cliente_id = request.POST.get('id_cliente')
        if cliente_id:
            try:
                venta.id_cliente = Cliente.objects.get(pk=cliente_id)
            except Cliente.DoesNotExist:
                messages.error(request, 'Cliente no encontrado')
                return redirect('Ventas')

        fecha = request.POST.get('fecha')
        if fecha:
            venta.fecha = fecha

        estado = request.POST.get('estado')
        if estado in dict(Venta.ESTADO_CHOICES):
            venta.estado = estado

        venta.observaciones = request.POST.get('observaciones', venta.observaciones)
        venta.save()
        messages.success(request, 'La venta ha sido modificada')
    return redirect('Ventas')


@login_required
def clientes_view(request):
    clientes = Cliente.objects.all().order_by('apellidos', 'nombre')
    context = {
        'Clientes': clientes,
        'form_cliente': AddClienteForm(),
        'form_editar_cliente': EditarClienteForm(),
    }
    return render(request, 'ventas/clientes.html', context)


@login_required
def add_clientes_view(request):
    if request.method == 'POST':
        form = AddClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El cliente ha sido agregado')
        else:
            messages.error(request, 'Revisa los datos del cliente')
    return redirect('Clientes')


@login_required
def edit_clientes_view(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('id_personal_editar')
        if cliente_id:
            try:
                cliente = Cliente.objects.get(pk=cliente_id)
                form = EditarClienteForm(request.POST, instance=cliente)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'El cliente ha sido modificado')
                else:
                    messages.error(request, 'Revisa los datos del cliente')
            except Cliente.DoesNotExist:
                messages.error(request, 'Cliente no encontrado')
    return redirect('Clientes')


@login_required
def delete_clientes_view(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('id_personal_eliminar')
        if cliente_id:
            try:
                cliente = Cliente.objects.get(pk=cliente_id)
                if Venta.objects.filter(id_cliente=cliente).exists():
                    messages.error(request, 'No se puede eliminar el cliente porque tiene ventas asociadas')
                else:
                    cliente.delete()
                    messages.success(request, 'El cliente ha sido eliminado')
            except Cliente.DoesNotExist:
                messages.error(request, 'Cliente no encontrado')
    return redirect('Clientes')


@login_required
def cursos_view(request):
    cursos = Curso.objects.all().order_by('codigo')
    context = {
        'Cursos': cursos,
        'form_curso': AddCursoForm(),
        'form_editar_curso': EditarCursoForm(),
    }
    return render(request, 'ventas/cursos.html', context)


@login_required
def add_curso_view(request):
    if request.method == 'POST':
        form = AddCursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El curso ha sido agregado')
        else:
            messages.error(request, 'Revisa los datos del curso')
    return redirect('Cursos')


@login_required
def delete_curso_view(request):
    if request.method == 'POST':
        curso_id = request.POST.get('id_curso_eliminar')
        if curso_id:
            try:
                curso = Curso.objects.get(pk=curso_id)
                if VentaDetalle.objects.filter(id_curso=curso).exists():
                    messages.error(request, 'No se puede eliminar el curso porque tiene ventas asociadas')
                else:
                    curso.delete()
                    messages.success(request, 'El curso ha sido eliminado')
            except Curso.DoesNotExist:
                messages.error(request, 'Curso no encontrado')
    return redirect('Cursos')


@login_required
def edit_curso_view(request):
    if request.method == 'POST':
        curso_id = request.POST.get('id_curso_editar')
        if curso_id:
            try:
                curso = Curso.objects.get(pk=curso_id)
                form = EditarCursoForm(request.POST, instance=curso)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'El curso ha sido modificado')
                else:
                    messages.error(request, 'Revisa los datos del curso')
            except Curso.DoesNotExist:
                messages.error(request, 'Curso no encontrado')
    return redirect('Cursos')


@login_required
def delete_venta_view(request):
    if request.method == 'POST':
        venta_id = request.POST.get('id_venta_eliminar')
        if venta_id:
            try:
                venta = Venta.objects.get(pk=venta_id)
                VentaDetalle.objects.filter(id_venta=venta).delete()
                venta.delete()
                messages.success(request, 'La venta y su contenido se ha eliminado')
            except Venta.DoesNotExist:
                messages.error(request, 'Venta no encontrada')
    return redirect('Ventas')


# Alias legacy inventario/producto
inventario_view = cursos_view
add_producto_view = add_curso_view
delete_producto_view = delete_curso_view
edit_producto_view = edit_curso_view
