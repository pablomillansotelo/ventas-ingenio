from django import forms
from ventas.models import Cliente, Producto, Venta, VentaDetalle
from datetime import date

class AddClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ('id_cliente', 'nombre', 'apellidos', 'direccion', 'email', 'telefono')
        labels = {
            'id_cliente':'ID',
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'direccion': 'Direccion',
            'email': 'Email',
            'telefono': 'Telefono',
        }


class EditarClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ('id_cliente', 'nombre', 'apellidos', 'direccion', 'email', 'telefono')
        labels = {
            'id_cliente': 'ID',
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'direccion': 'Direccion',
            'email': 'Email',
            'telefono': 'Telefono',
        }
        widgets = {
            'id_cliente': forms.TextInput(attrs={'type': 'text', 'id': 'id_cliente_editar'}),
            'nombre': forms.TextInput(attrs={'type': 'text', 'id': 'nombre_editar'}),
            'apellidos': forms.TextInput(attrs={'type': 'text', 'id': 'apellidos_editar'}),
            'direccion': forms.TextInput(attrs={'type': 'text', 'id': 'direccion_editar'}),
            'email': forms.TextInput(attrs={'type': 'text', 'id': 'email_editar'}),
            'telefono': forms.TextInput(attrs={'type': 'text', 'id': 'telefono_editar'}),
        }


class AddProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('id_producto', 'producto', 'precio_unitario')
        labels = {
            'id_producto':'ID',
            'producto': 'Producto',
            'precio_unitario': 'Precio Unitario',
        }


class EditarProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('id_producto', 'producto', 'precio_unitario')
        labels = {
            'id_producto': 'ID',
            'producto': 'Producto',
            'precio_unitario': 'Precio Unitario',
        }
        widgets = {
            'id_producto': forms.TextInput(attrs={'type': 'text', 'id': 'id_producto_editar'}),
            'producto': forms.TextInput(attrs={'type': 'text', 'id': 'producto_editar'}),
            'precio_producto': forms.NumberInput(attrs={'type': 'number', 'id': 'precio_unitario_editar'}),
        }


class EditarVentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ('id_venta', 'id_cliente', 'fecha')
        labels = {
            'id_venta': 'ID',
            'id_cliente': 'Cliente',
            'fecha': 'Fecha',
        }
        widgets = {
            'id_venta': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_venta_editar'}),
            'id_cliente': forms.Select(attrs={'class': 'form-control', 'id': 'id_cliente_editar'}),
            #'fecha':  forms.TextInput(attrs={'type': 'text', 'id': 'fecha_editar'}),
            'fecha': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date', 'id': 'fecha_editar'}),
        }

class AddVentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ('id_venta', 'id_cliente', 'fecha')
        labels = {
            'id_venta': 'ID',
            'id_cliente': 'Cliente',
            'fecha': 'Fecha',
        }
        widgets = {
            'id_venta': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'id_venta_add'}),
            'id_cliente': forms.Select(attrs={'class': 'form-control', 'id': 'id_cliente_add'}),
            'fecha': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date', 'id': 'fecha_add', 'value': date.today()}),
        }

class AddVentaDetalleForm(forms.ModelForm):

    class Meta:
        model = VentaDetalle
        fields = ( 'id_producto', 'cantidad',  'descuento')
        labels = {
            'id_producto': 'Producto',
            'cantidad': 'Cantidad',
            'descuento': 'Descuento'
        }
        widgets = {
            'id_producto': forms.Select(attrs={'class': 'form-control', 'id': 'id_producto_add'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'cantidad_add'}),
            'descuento': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'descuento_add'}),
        }




