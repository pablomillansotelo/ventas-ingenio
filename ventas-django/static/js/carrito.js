let carrito = [];

function filtrarEdicionesPorCurso() {
    const cursoId = document.getElementById('id_curso_add')?.value;
    const selectEdicion = document.getElementById('id_edicion_add');
    if (!selectEdicion) return;

    Array.from(selectEdicion.options).forEach((opt, idx) => {
        if (idx === 0) {
            opt.hidden = false;
            return;
        }
        const cursoOpt = opt.dataset.curso;
        opt.hidden = cursoId && cursoOpt && cursoOpt !== cursoId;
    });
    selectEdicion.selectedIndex = 0;
}

function agregarCurso() {
    const id_curso = document.getElementById('id_curso_add').value;
    const id_edicion = document.getElementById('id_edicion_add').value;
    const select = document.getElementById('id_curso_add');
    const selectEd = document.getElementById('id_edicion_add');
    let nombre_curso = select.selectedOptions[0]?.text || '';
    if (id_edicion && selectEd.selectedOptions[0]) {
        nombre_curso += ' · ' + selectEd.selectedOptions[0].text.trim();
    }
    const cantidad = document.getElementById('cantidad_add').value;
    const descuento = document.getElementById('descuento_add').value;

    if (!id_curso || !cantidad) {
        Swal.fire({ text: 'Selecciona un curso y las plazas.', icon: 'warning', confirmButtonColor: '#c0392b' });
        return;
    }

    carrito.push({ id_curso, id_edicion, nombre_curso, cantidad, descuento });
    renderCarrito();

    select.selectedIndex = 0;
    if (selectEd) selectEd.selectedIndex = 0;
    document.getElementById('cantidad_add').value = '1';
    document.getElementById('descuento_add').value = '';
    filtrarEdicionesPorCurso();
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
            <td>${item.nombre_curso}</td>
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
    const observaciones = document.getElementById('observaciones_add').value;

    if (!id_cliente || !fecha || carrito.length === 0) {
        Swal.fire({ text: 'Completa cliente, fecha y al menos un curso.', icon: 'warning', confirmButtonColor: '#c0392b' });
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

    ['id_cliente_add', 'fecha_add', 'observaciones_add'].forEach((name, i) => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = [id_cliente, fecha, observaciones][i];
        form.appendChild(input);
    });

    carrito.forEach((item) => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'nplainArray[]';
        input.value = `${item.id_curso},${item.id_edicion || ''},${item.cantidad},${item.descuento || ''}`;
        form.appendChild(input);
    });

    document.body.appendChild(form);
    form.submit();
}

document.addEventListener('DOMContentLoaded', () => {
    renderCarrito();
    document.getElementById('id_curso_add')?.addEventListener('change', filtrarEdicionesPorCurso);
    const selectEd = document.getElementById('id_edicion_add');
    if (selectEd) {
        Array.from(selectEd.options).forEach((opt, idx) => {
            if (idx === 0) return;
            const match = opt.text.match(/^\[(\d+)\]/);
            if (match) opt.dataset.curso = match[1];
        });
    }
    filtrarEdicionesPorCurso();
});
