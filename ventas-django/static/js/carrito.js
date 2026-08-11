let carrito = [];

function agregarProducto() {
    const id_producto = document.getElementById('id_producto_add').value;
    const select = document.getElementById('id_producto_add');
    const nombre_producto = select.selectedOptions[0]?.text || '';
    const cantidad = document.getElementById('cantidad_add').value;
    const descuento = document.getElementById('descuento_add').value;

    if (!id_producto || !cantidad) {
        Swal.fire({ text: 'Selecciona un producto y la cantidad.', icon: 'warning', confirmButtonColor: '#c0392b' });
        return;
    }

    carrito.push({ id_producto, nombre_producto, cantidad, descuento });
    renderCarrito();

    select.selectedIndex = 0;
    document.getElementById('cantidad_add').value = '1';
    document.getElementById('descuento_add').value = '';
}

function renderCarrito() {
    const tbody = document.querySelector('#tblProducts tbody');
    const empty = document.getElementById('carritoEmpty');
    if (!tbody) return;

    tbody.innerHTML = '';
    if (carrito.length === 0) {
        empty?.classList.remove('d-none');
        return;
    }
    empty?.classList.add('d-none');

    carrito.forEach((item, idx) => {
        tbody.innerHTML += `<tr>
            <td>${item.nombre_producto}</td>
            <td class="text-center">${item.cantidad}</td>
            <td class="text-end">${item.descuento ? '$' + item.descuento : '—'}</td>
            <td class="text-end">
                <button type="button" class="btn btn-icon btn-icon-delete" onclick="eliminarItemCarrito(${idx})" title="Quitar">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        </tr>`;
    });
}

function eliminarItemCarrito(idx) {
    carrito.splice(idx, 1);
    renderCarrito();
}

function pagar_carrito() {
    const id_cliente = document.getElementById('id_cliente_add').value;
    const fecha = document.getElementById('fecha_add').value;

    if (!id_cliente || !fecha || carrito.length === 0) {
        Swal.fire({ text: 'Completa cliente, fecha y al menos un producto.', icon: 'warning', confirmButtonColor: '#c0392b' });
        return;
    }

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = document.getElementById('carritoFormAction').value;

    const csrf = document.createElement('input');
    csrf.type = 'hidden';
    csrf.name = 'csrfmiddlewaretoken';
    csrf.value = document.querySelector('[name=csrfmiddlewaretoken]').value;
    form.appendChild(csrf);

    const clienteInput = document.createElement('input');
    clienteInput.type = 'hidden';
    clienteInput.name = 'id_cliente_add';
    clienteInput.value = id_cliente;
    form.appendChild(clienteInput);

    const fechaInput = document.createElement('input');
    fechaInput.type = 'hidden';
    fechaInput.name = 'fecha_add';
    fechaInput.value = fecha;
    form.appendChild(fechaInput);

    carrito.forEach((item) => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'nplainArray[]';
        input.value = `${item.id_producto},${item.cantidad},${item.descuento}`;
        form.appendChild(input);
    });

    document.body.appendChild(form);
    form.submit();
}

document.addEventListener('DOMContentLoaded', renderCarrito);
