function agregar_productos(){
    var producto = {
        id_producto: document.getElementById("id_producto_add").value,
        cantidad: document.getElementById("cantidad_add").value,
        descuento: document.getElementById("descuento_add").value
    };
    vents.add(producto);
}