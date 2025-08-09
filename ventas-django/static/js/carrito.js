let carrito = [];

function agregarProducto() {
    const id_producto = document.getElementById('id_id_producto').value;
    const nombre_producto = document.getElementById('id_id_producto').selectedOptions[0].text;
    const cantidad = document.getElementById('id_cantidad').value;
    const descuento = document.getElementById('id_descuento').value;

    carrito.push({id_producto, nombre_producto, cantidad, descuento});
    renderCarrito();
}

function renderCarrito() {
    const tbody = document.querySelector('#tblProducts tbody');
    tbody.innerHTML = '';
    carrito.forEach((item, idx) => {
        tbody.innerHTML += `<tr>
            <td>${item.nombre_producto}</td>
            <td>${item.cantidad}</td>
            <td>${item.descuento}</td>
            <td><button type="button" onclick="eliminarProducto(${idx})">Eliminar</button></td>
        </tr>`;
    });
}

function eliminarProducto(idx) {
    carrito.splice(idx, 1);
    renderCarrito();
}

function pagar_carrito() {
    const id_cliente = document.getElementById('id_id_cliente').value;
    const fecha = document.getElementById('id_fecha').value;

    // Crea un formulario y lo envía por POST
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = "{% url 'AddCarrito' %}";

    // CSRF token
    const csrf = document.createElement('input');
    csrf.type = 'hidden';
    csrf.name = 'csrfmiddlewaretoken';
    csrf.value = '{{ csrf_token }}';
    form.appendChild(csrf);

    // Cliente y fecha
    form.innerHTML += `<input type="hidden" name="id_cliente_add" value="${id_cliente}">`;
    form.innerHTML += `<input type="hidden" name="fecha_add" value="${fecha}">`;

    // Productos
    carrito.forEach((item, idx) => {
        form.innerHTML += `<input type="hidden" name="nplainArray[]" value="${item.id_producto},${item.cantidad},${item.descuento}">`;
    });

    document.body.appendChild(form);
    form.submit();
}
