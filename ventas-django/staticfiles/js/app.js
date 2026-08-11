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

function editarVenta(idVenta, idCliente, fecha, estado, observaciones) {
    setFieldValue('id_venta_editar', idVenta);
    setFieldValue('id_cliente_editar', idCliente);
    setFieldValue('fecha_editar', fecha);
    setFieldValue('estado_editar', estado || 'confirmada');
    setFieldValue('observaciones_editar', observaciones || '');
}

function eliminarVenta(idVenta) {
    setFieldValue('id_venta_eliminar', idVenta);
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
