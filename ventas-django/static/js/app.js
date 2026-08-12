function setFieldValue(id, value) {
    const el = document.getElementById(id);
    if (el) el.value = value ?? '';
}

function setCheckboxValue(id, checked) {
    const el = document.getElementById(id);
    if (el) el.checked = checked === true || checked === 'true';
}

function editarPersonal(id, nombre, apellidos, direccion, email, telefono, curp, empresa) {
    setFieldValue('id_personal_editar', id);
    setFieldValue('nombre_editar', nombre);
    setFieldValue('apellidos_editar', apellidos);
    setFieldValue('direccion_editar', direccion);
    setFieldValue('email_editar', email);
    setFieldValue('telefono_editar', telefono);
    setFieldValue('curp_editar', curp);
    setFieldValue('empresa_editar', empresa);
}

function eliminarPersonal(id) {
    setFieldValue('id_personal_eliminar', id);
}

function editarCurso(id, codigo, nombre, descripcion, duracion, modalidad, precio, activo) {
    setFieldValue('id_curso_editar', id);
    setFieldValue('codigo_editar', codigo);
    setFieldValue('nombre_curso_editar', nombre);
    setFieldValue('descripcion_editar', descripcion);
    setFieldValue('duracion_horas_editar', duracion);
    setFieldValue('modalidad_editar', modalidad);
    setFieldValue('precio_lista_editar', precio);
    setCheckboxValue('activo_editar', activo);
}

function eliminarCurso(id) {
    setFieldValue('id_curso_eliminar', id);
}

function editarVenta(idVenta, idCliente, fecha, estado, estadoPago, observaciones) {
    setFieldValue('id_venta_editar', idVenta);
    setFieldValue('id_cliente_editar', idCliente);
    setFieldValue('fecha_editar', fecha);
    setFieldValue('estado_editar', estado || 'confirmada');
    setFieldValue('estado_pago_editar', estadoPago || 'pendiente');
    setFieldValue('observaciones_editar', observaciones || '');
}

function eliminarVenta(idVenta) {
    setFieldValue('id_venta_eliminar', idVenta);
}

function editarVendedor(id, userId, nombre, email, telefono, comision, activo) {
    setFieldValue('id_vendedor_editar', id);
    setFieldValue('user_id_editar', userId);
    setFieldValue('nombre_vendedor_editar', nombre);
    setFieldValue('email_vendedor_editar', email);
    setFieldValue('telefono_vendedor_editar', telefono);
    setFieldValue('comision_editar', comision);
    setCheckboxValue('activo_vendedor_editar', activo);
}

function eliminarVendedor(id) {
    setFieldValue('id_vendedor_eliminar', id);
}

function editarEdicion(id, cursoId, codigo, inicio, fin, cupo, precio, estado, activo) {
    setFieldValue('id_edicion_editar', id);
    setFieldValue('id_curso_edicion_editar', cursoId);
    setFieldValue('codigo_edicion_editar', codigo);
    setFieldValue('fecha_inicio_editar', inicio);
    setFieldValue('fecha_fin_editar', fin || '');
    setFieldValue('cupo_maximo_editar', cupo);
    setFieldValue('precio_edicion_editar', precio);
    setFieldValue('estado_edicion_editar', estado);
    setCheckboxValue('activo_edicion_editar', activo);
}

function eliminarEdicion(id) {
    setFieldValue('id_edicion_eliminar', id);
}

function editarPago(id, ventaId, monto, metodo, referencia, fecha, estado) {
    setFieldValue('id_pago_editar', id);
    setFieldValue('id_venta_pago_editar', ventaId);
    setFieldValue('monto_pago_editar', monto);
    setFieldValue('metodo_pago_editar', metodo);
    setFieldValue('referencia_pago_editar', referencia);
    setFieldValue('fecha_pago_editar', fecha);
    setFieldValue('estado_pago_reg_editar', estado);
}

function eliminarPago(id) {
    setFieldValue('id_pago_eliminar', id);
}

function editarInscripcion(id, estado) {
    setFieldValue('id_inscripcion_editar', id);
    setFieldValue('estado_inscripcion_editar', estado);
}

function eliminarInscripcion(id) {
    setFieldValue('id_inscripcion_eliminar', id);
}

function showMessages(messages) {
    if (!messages?.length || typeof Swal === 'undefined') return;
    messages.forEach((msg) => Swal.fire({ text: msg, icon: 'info', confirmButtonColor: '#c0392b' }));
}

function initSidebar() {
    const sidebar = document.getElementById('appSidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    const toggle = document.getElementById('sidebarToggle');
    if (!sidebar || !toggle) return;

    const close = () => {
        sidebar.classList.remove('show');
        backdrop?.classList.remove('show');
    };

    toggle.addEventListener('click', () => {
        sidebar.classList.toggle('show');
        backdrop?.classList.toggle('show');
    });

    backdrop?.addEventListener('click', close);
    sidebar.querySelectorAll('.sidebar-link').forEach((link) => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 992) close();
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initSidebar();
    const data = document.getElementById('django-messages-data');
    if (data) {
        try { showMessages(JSON.parse(data.textContent)); }
        catch (e) { console.error('Error al mostrar mensajes', e); }
    }
});
