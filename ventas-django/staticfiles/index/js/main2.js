/*$( document ).ready(function() {
    // Handler for .ready() called.
    alert('Todo bien');
  });*/


function editarProduct(id, precio, descripcion, costo, cantidad, categoria, servicio) {
  document.getElementById("id_producto_editar").value = id;
  document.getElementById("precio_editar").value = precio;
  document.getElementById("descripcion_editar").value = descripcion;
  document.getElementById("costo_editar").value = costo;
  document.getElementById("cantidad_editar").value = cantidad;
  document.getElementById("categoria_editar").value = categoria;
  if (servicio=='True'){
    document.getElementById('servicio_editar').checked=true;
  }
}


function eliminarCorrectivo(id) {
  document.getElementById("id_correctivo_eliminar").value = id;
}

function eliminarProducto(id) {
  document.getElementById("id_producto_eliminar").value = id;
}

function editarPersonal(id, nombre, apellidos, direccion, email, telefono) {

  document.getElementById("id_personal_editar").value = id;
  document.getElementById("nombre_editar").value = nombre;
  document.getElementById("apellidos_editar").value = apellidos;
  document.getElementById("direccion_editar").value = direccion;
  document.getElementById("email_editar").value = email;
  document.getElementById("telefono_editar").value = telefono;

}

function eliminarPersonal(id) {
  document.getElementById("id_personal_eliminar").value = id;
}


function seleccionarCliente(id, nombre){
 document.getElementById("id_cliente").value = id;
 document.getElementById("cliente").value = nombre;
}


function eliminarProducto(id) {
  document.getElementById("id_producto_eliminar").value = id;
}

function eliminarProducto(id) {
  document.getElementById("id_producto_eliminar").value = id;
}

function editarProducto(id, producto, precio_unitario) {

  document.getElementById("id_producto_editar").value = id;
  document.getElementById("producto_editar").value = producto;
  document.getElementById("precio_unitario_editar").value = precio_unitario;

}

function editarVenta(id, producto, precio_unitario) {

  document.getElementById("id_venta_editar").value = id;
  document.getElementById("id_producto_editar").value = producto;
  document.getElementById("fecha_editar").value = precio_unitario;

}

function eliminarVenta(id) {
  document.getElementById("id_venta_eliminar").value = id;
}



$(document).ready(function () {

  $('#myTable').DataTable({
    "language": {
      "url": "../static/index/js/idiom.json"},
    "lengthMenu": [[10, 25, 50], [10, 25, 50]],
    dom: 'Bfrtip',
    buttons: [
      { extend: 'csv' },
      { extend: 'print'},
    ]
  });
  $('#table2').DataTable({
    "language": {
      "url": "../static/index/js/idiom.json"},
    "lengthMenu": [[10, 25, 50], [10, 25, 50]],
    dom: 'Bfrtip',
    buttons: [
      { extend: 'csv' },
      { extend: 'print'},
    ]
  });
  $('#table3').DataTable({
    "language": {
      "url": "../static/index/js/idiom.json"},
    "lengthMenu": [[10, 25, 50], [10, 25, 50]],
    dom: 'Bfrtip',
    buttons: [
      { extend: 'csv' },
      { extend: 'print'},
    ]
  });
});
 