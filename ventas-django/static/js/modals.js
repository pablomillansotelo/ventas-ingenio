function setFieldValue(id, value) {
    const el = document.getElementById(id);
    if (el) {
        el.value = value ?? '';
    }
}

function editarPersonal(id, nombre, apellidos, direccion, email, telefono) {
    setFieldValue('id_personal_editar', id);
    setFieldValue('nombre_editar', nombre);
    setFieldValue('apellidos_editar', apellidos);
    setFieldValue('direccion_editar', direccion);
    setFieldValue('email_editar', email);
    setFieldValue('telefono_editar', telefono);
}

function eliminarPersonal(id) {
    setFieldValue('id_personal_eliminar', id);
}

function editarProducto(id, producto, precio) {
    setFieldValue('id_producto_editar', id);
    setFieldValue('producto_editar', producto);
    setFieldValue('precio_unitario_editar', precio);
}

function eliminarProductoInventario(id) {
    setFieldValue('id_producto_eliminar', id);
}

function editarVenta(idVenta, idCliente, fecha) {
    setFieldValue('id_venta_editar', idVenta);
    setFieldValue('id_cliente_editar', idCliente);
    setFieldValue('fecha_editar', fecha);
}

function eliminarVenta(idVenta) {
    setFieldValue('id_venta_eliminar', idVenta);
}

function showMessages(messages) {
    if (typeof Swal === 'undefined' || !messages || !messages.length) {
        return;
    }
    messages.forEach(function (message) {
        Swal.fire({ text: message });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const data = document.getElementById('django-messages-data');
    if (data) {
        try {
            showMessages(JSON.parse(data.textContent));
        } catch (e) {
            console.error('No se pudieron mostrar los mensajes Django', e);
        }
    }
});
