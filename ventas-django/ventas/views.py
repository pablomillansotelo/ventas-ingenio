from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import (
    AddClienteForm,
    AddCursoForm,
    AddEdicionForm,
    AddInscripcionForm,
    AddPagoForm,
    AddVendedorForm,
    AddVentaDetalleForm,
    AddVentaForm,
    EditarClienteForm,
    EditarCursoForm,
    EditarEdicionForm,
    EditarInscripcionForm,
    EditarPagoForm,
    EditarVendedorForm,
    EditarVentaForm,
)
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


def _vendedor_actual(request):
    return Vendedor.obtener_o_crear_desde_usuario(request.user)


def _parse_carrito_item(item):
    partes = item.split(',')
    if len(partes) == 3:
        return partes[0], None, partes[1], partes[2]
    if len(partes) >= 4:
        return partes[0], partes[1] or None, partes[2], partes[3]
    raise ValueError('Formato de carrito inválido')


@login_required
def dashboard_view(request):
    hoy = timezone.localdate()
    inicio_mes = hoy.replace(day=1)
    ventas_mes_qs = Venta.objects.filter(
        fecha__gte=inicio_mes, estado=Venta.ESTADO_CONFIRMADA,
    ).prefetch_related('ventadetalle_set')
    context = {
        'total_clientes': Cliente.objects.filter(activo=True).count(),
        'total_cursos': Curso.objects.filter(activo=True).count(),
        'ediciones_abiertas': EdicionCurso.objects.filter(
            activo=True,
            estado__in=[EdicionCurso.ESTADO_PROGRAMADA, EdicionCurso.ESTADO_EN_CURSO],
        ).count(),
        'ventas_mes_count': ventas_mes_qs.count(),
        'ventas_mes_monto': sum(v.monto for v in ventas_mes_qs),
        'inscripciones_activas': Inscripcion.objects.filter(estado=Inscripcion.ESTADO_ACTIVA).count(),
        'pagos_pendientes': Venta.objects.filter(estado_pago=Venta.PAGO_PENDIENTE).count(),
        'ultimas_ventas': Venta.objects.select_related('id_cliente', 'id_vendedor').order_by('-id_venta')[:5],
    }
    return render(request, 'ventas/dashboard.html', context)


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
        cliente = Cliente.objects.get(pk=id_cliente_add, activo=True)
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
                id_curso, id_edicion, cantidad, descuento = _parse_carrito_item(item)
                curso = Curso.objects.get(pk=id_curso, activo=True)
                edicion = None
                if id_edicion:
                    edicion = EdicionCurso.objects.select_for_update().get(
                        pk=id_edicion, activo=True, id_curso=curso,
                    )
                    edicion.reservar_cupo(int(cantidad))

                precio = edicion.precio_aplicable if edicion else curso.precio_lista
                detalle = VentaDetalle.objects.create(
                    id_venta=venta,
                    id_curso=curso,
                    id_edicion=edicion,
                    cantidad=cantidad,
                    precio_unitario=precio,
                    descuento=descuento or None,
                )
                Inscripcion.objects.create(
                    id_cliente=cliente,
                    id_curso=curso,
                    id_edicion=edicion,
                    id_venta_det=detalle,
                    estado=Inscripcion.ESTADO_ACTIVA,
                )
    except (Curso.DoesNotExist, EdicionCurso.DoesNotExist):
        messages.error(request, 'Uno de los cursos o ediciones no está disponible')
        return redirect('Carrito')
    except ValueError as exc:
        messages.error(request, str(exc))
        return redirect('Carrito')
    except Exception:
        messages.error(request, 'No se pudo registrar la venta')
        return redirect('Carrito')

    messages.success(request, f'Venta {venta.folio} registrada correctamente')
    return redirect('Ventas')


@login_required
def ventas_view(request):
    ventas = Venta.objects.select_related('id_cliente', 'id_vendedor').prefetch_related(
        'ventadetalle_set__id_curso', 'ventadetalle_set__id_edicion', 'pago_set',
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

        estado_pago = request.POST.get('estado_pago')
        if estado_pago in dict(Venta.ESTADO_PAGO_CHOICES):
            venta.estado_pago = estado_pago

        venta.observaciones = request.POST.get('observaciones', venta.observaciones)
        venta.save()
        messages.success(request, 'La venta ha sido modificada')
    return redirect('Ventas')


@login_required
def delete_venta_view(request):
    if request.method == 'POST':
        venta_id = request.POST.get('id_venta_eliminar')
        if venta_id:
            try:
                with transaction.atomic():
                    venta = Venta.objects.get(pk=venta_id)
                    for det in venta.ventadetalle_set.select_related('id_edicion'):
                        if det.id_edicion_id:
                            ed = EdicionCurso.objects.select_for_update().get(pk=det.id_edicion_id)
                            ed.cupo_ocupado = max(0, ed.cupo_ocupado - det.cantidad)
                            ed.save(update_fields=['cupo_ocupado'])
                    Inscripcion.objects.filter(id_venta_det__id_venta=venta).update(
                        estado=Inscripcion.ESTADO_CANCELADA,
                    )
                    Pago.objects.filter(id_venta=venta).delete()
                    VentaDetalle.objects.filter(id_venta=venta).delete()
                    venta.delete()
                messages.success(request, 'La venta y su contenido se ha eliminado')
            except Venta.DoesNotExist:
                messages.error(request, 'Venta no encontrada')
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
def vendedores_view(request):
    vendedores = Vendedor.objects.annotate(
        num_ventas=Count('ventas'),
    ).order_by('nombre')
    context = {
        'Vendedores': vendedores,
        'form_vendedor': AddVendedorForm(),
        'form_editar_vendedor': EditarVendedorForm(),
    }
    return render(request, 'ventas/vendedores.html', context)


@login_required
def add_vendedor_view(request):
    if request.method == 'POST':
        form = AddVendedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendedor registrado')
        else:
            messages.error(request, 'Revisa los datos del vendedor')
    return redirect('Vendedores')


@login_required
def edit_vendedor_view(request):
    if request.method == 'POST':
        vendedor_id = request.POST.get('id_vendedor_editar')
        if vendedor_id:
            try:
                vendedor = Vendedor.objects.get(pk=vendedor_id)
                form = EditarVendedorForm(request.POST, instance=vendedor)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Vendedor actualizado')
                else:
                    messages.error(request, 'Revisa los datos del vendedor')
            except Vendedor.DoesNotExist:
                messages.error(request, 'Vendedor no encontrado')
    return redirect('Vendedores')


@login_required
def delete_vendedor_view(request):
    if request.method == 'POST':
        vendedor_id = request.POST.get('id_vendedor_eliminar')
        if vendedor_id:
            try:
                vendedor = Vendedor.objects.get(pk=vendedor_id)
                if Venta.objects.filter(id_vendedor=vendedor).exists():
                    messages.error(request, 'No se puede eliminar: tiene ventas asociadas')
                else:
                    vendedor.delete()
                    messages.success(request, 'Vendedor eliminado')
            except Vendedor.DoesNotExist:
                messages.error(request, 'Vendedor no encontrado')
    return redirect('Vendedores')


@login_required
def cursos_view(request):
    cursos = Curso.objects.annotate(num_ediciones=Count('ediciones')).order_by('codigo')
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
def ediciones_view(request):
    ediciones = EdicionCurso.objects.select_related('id_curso').order_by('-fecha_inicio')
    context = {
        'Ediciones': ediciones,
        'form_edicion': AddEdicionForm(),
        'form_editar_edicion': EditarEdicionForm(),
    }
    return render(request, 'ventas/ediciones.html', context)


@login_required
def add_edicion_view(request):
    if request.method == 'POST':
        form = AddEdicionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Edición creada')
        else:
            messages.error(request, 'Revisa los datos de la edición')
    return redirect('Ediciones')


@login_required
def edit_edicion_view(request):
    if request.method == 'POST':
        edicion_id = request.POST.get('id_edicion_editar')
        if edicion_id:
            try:
                edicion = EdicionCurso.objects.get(pk=edicion_id)
                form = EditarEdicionForm(request.POST, instance=edicion)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Edición actualizada')
                else:
                    messages.error(request, 'Revisa los datos de la edición')
            except EdicionCurso.DoesNotExist:
                messages.error(request, 'Edición no encontrada')
    return redirect('Ediciones')


@login_required
def delete_edicion_view(request):
    if request.method == 'POST':
        edicion_id = request.POST.get('id_edicion_eliminar')
        if edicion_id:
            try:
                edicion = EdicionCurso.objects.get(pk=edicion_id)
                if VentaDetalle.objects.filter(id_edicion=edicion).exists():
                    messages.error(request, 'No se puede eliminar: tiene ventas asociadas')
                else:
                    edicion.delete()
                    messages.success(request, 'Edición eliminada')
            except EdicionCurso.DoesNotExist:
                messages.error(request, 'Edición no encontrada')
    return redirect('Ediciones')


@login_required
def pagos_view(request):
    pagos = Pago.objects.select_related('id_venta', 'id_venta__id_cliente').order_by('-fecha_pago')
    ventas_pendientes = Venta.objects.filter(
        estado=Venta.ESTADO_CONFIRMADA,
        estado_pago__in=[Venta.PAGO_PENDIENTE, Venta.PAGO_PARCIAL],
    ).select_related('id_cliente')
    context = {
        'Pagos': pagos,
        'VentasPendientes': ventas_pendientes,
        'form_pago': AddPagoForm(),
        'form_editar_pago': EditarPagoForm(),
    }
    return render(request, 'ventas/pagos.html', context)


@login_required
def add_pago_view(request):
    if request.method == 'POST':
        form = AddPagoForm(request.POST)
        if form.is_valid():
            pago = form.save()
            messages.success(request, f'Pago #{pago.id_pago} registrado')
        else:
            messages.error(request, 'Revisa los datos del pago')
    return redirect('Pagos')


@login_required
def edit_pago_view(request):
    if request.method == 'POST':
        pago_id = request.POST.get('id_pago_editar')
        if pago_id:
            try:
                pago = Pago.objects.get(pk=pago_id)
                form = EditarPagoForm(request.POST, instance=pago)
                if form.is_valid():
                    form.save()
                    pago.id_venta.actualizar_estado_pago()
                    messages.success(request, 'Pago actualizado')
                else:
                    messages.error(request, 'Revisa los datos del pago')
            except Pago.DoesNotExist:
                messages.error(request, 'Pago no encontrado')
    return redirect('Pagos')


@login_required
def delete_pago_view(request):
    if request.method == 'POST':
        pago_id = request.POST.get('id_pago_eliminar')
        if pago_id:
            try:
                pago = Pago.objects.get(pk=pago_id)
                venta = pago.id_venta
                pago.delete()
                venta.actualizar_estado_pago()
                messages.success(request, 'Pago eliminado')
            except Pago.DoesNotExist:
                messages.error(request, 'Pago no encontrado')
    return redirect('Pagos')


@login_required
def inscripciones_view(request):
    inscripciones = Inscripcion.objects.select_related(
        'id_cliente', 'id_curso', 'id_edicion',
    ).order_by('-fecha_inscripcion')
    context = {
        'Inscripciones': inscripciones,
        'form_inscripcion': AddInscripcionForm(),
        'form_editar_inscripcion': EditarInscripcionForm(),
    }
    return render(request, 'ventas/inscripciones.html', context)


@login_required
def add_inscripcion_view(request):
    if request.method == 'POST':
        form = AddInscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save()
            if inscripcion.id_edicion_id:
                try:
                    inscripcion.id_edicion.reservar_cupo(1)
                except ValueError:
                    inscripcion.delete()
                    messages.error(request, 'No hay cupo disponible en la edición')
                    return redirect('Inscripciones')
            messages.success(request, 'Inscripción registrada')
        else:
            messages.error(request, 'Revisa los datos de la inscripción')
    return redirect('Inscripciones')


@login_required
def edit_inscripcion_view(request):
    if request.method == 'POST':
        inscripcion_id = request.POST.get('id_inscripcion_editar')
        if inscripcion_id:
            try:
                inscripcion = Inscripcion.objects.get(pk=inscripcion_id)
                form = EditarInscripcionForm(request.POST, instance=inscripcion)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Inscripción actualizada')
                else:
                    messages.error(request, 'Revisa los datos')
            except Inscripcion.DoesNotExist:
                messages.error(request, 'Inscripción no encontrada')
    return redirect('Inscripciones')


@login_required
def delete_inscripcion_view(request):
    if request.method == 'POST':
        inscripcion_id = request.POST.get('id_inscripcion_eliminar')
        if inscripcion_id:
            try:
                inscripcion = Inscripcion.objects.get(pk=inscripcion_id)
                inscripcion.estado = Inscripcion.ESTADO_CANCELADA
                inscripcion.save(update_fields=['estado'])
                messages.success(request, 'Inscripción cancelada')
            except Inscripcion.DoesNotExist:
                messages.error(request, 'Inscripción no encontrada')
    return redirect('Inscripciones')


# Alias legacy inventario/producto
inventario_view = cursos_view
add_producto_view = add_curso_view
delete_producto_view = delete_curso_view
edit_producto_view = edit_curso_view
