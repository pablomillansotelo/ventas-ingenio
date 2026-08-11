from django import forms
from ventas.models import Cliente, Producto, Venta, VentaDetalle
from datetime import date

INPUT = 'form-control'
SELECT = 'form-select'


class AddClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ('nombre', 'apellidos', 'direccion', 'email', 'telefono')
        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'direccion': 'Dirección',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Apellidos'}),
            'direccion': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Dirección'}),
            'email': forms.EmailInput(attrs={'class': INPUT, 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': INPUT, 'placeholder': '5551234567'}),
        }


class EditarClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ('nombre', 'apellidos', 'direccion', 'email', 'telefono')
        labels = AddClienteForm.Meta.labels
        widgets = {
            'nombre': forms.TextInput(attrs={'class': INPUT, 'id': 'nombre_editar'}),
            'apellidos': forms.TextInput(attrs={'class': INPUT, 'id': 'apellidos_editar'}),
            'direccion': forms.TextInput(attrs={'class': INPUT, 'id': 'direccion_editar'}),
            'email': forms.EmailInput(attrs={'class': INPUT, 'id': 'email_editar'}),
            'telefono': forms.TextInput(attrs={'class': INPUT, 'id': 'telefono_editar'}),
        }


class AddProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('producto', 'precio_unitario')
        labels = {
            'producto': 'Nombre del producto',
            'precio_unitario': 'Precio unitario',
        }
        widgets = {
            'producto': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Ej. Curso de Python'}),
            'precio_unitario': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
        }


class EditarProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('producto', 'precio_unitario')
        labels = AddProductoForm.Meta.labels
        widgets = {
            'producto': forms.TextInput(attrs={'class': INPUT, 'id': 'producto_editar'}),
            'precio_unitario': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'id': 'precio_unitario_editar'}),
        }


class EditarVentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ('id_cliente', 'fecha')
        labels = {
            'id_cliente': 'Cliente',
            'fecha': 'Fecha de venta',
        }
        widgets = {
            'id_cliente': forms.Select(attrs={'class': SELECT, 'id': 'id_cliente_editar'}),
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'class': INPUT, 'type': 'date', 'id': 'fecha_editar'}),
        }


class AddVentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ('id_cliente', 'fecha')
        labels = EditarVentaForm.Meta.labels
        widgets = {
            'id_cliente': forms.Select(attrs={'class': SELECT, 'id': 'id_cliente_add'}),
            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': INPUT, 'type': 'date', 'id': 'fecha_add', 'value': date.today().isoformat()},
            ),
        }


class AddVentaDetalleForm(forms.ModelForm):

    class Meta:
        model = VentaDetalle
        fields = ('id_producto', 'cantidad', 'descuento')
        labels = {
            'id_producto': 'Producto',
            'cantidad': 'Cantidad',
            'descuento': 'Descuento ($)',
        }
        widgets = {
            'id_producto': forms.Select(attrs={'class': SELECT, 'id': 'id_producto_add'}),
            'cantidad': forms.NumberInput(attrs={'class': INPUT, 'min': '1', 'id': 'cantidad_add', 'value': '1'}),
            'descuento': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'min': '0', 'id': 'descuento_add', 'placeholder': '0.00'}),
        }
