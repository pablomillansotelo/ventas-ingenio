from django import forms
from ventas.models import Cliente, Producto, Venta, VentaDetalle
from datetime import date

INPUT_CLASS = 'form-control'


class AddClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ('nombre', 'apellidos', 'direccion', 'email', 'telefono')
        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'direccion': 'Direccion',
            'email': 'Email',
            'telefono': 'Telefono',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'apellidos': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'direccion': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS}),
            'telefono': forms.TextInput(attrs={'class': INPUT_CLASS}),
        }


class EditarClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ('nombre', 'apellidos', 'direccion', 'email', 'telefono')
        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'direccion': 'Direccion',
            'email': 'Email',
            'telefono': 'Telefono',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'type': 'text', 'id': 'nombre_editar', 'class': INPUT_CLASS}),
            'apellidos': forms.TextInput(attrs={'type': 'text', 'id': 'apellidos_editar', 'class': INPUT_CLASS}),
            'direccion': forms.TextInput(attrs={'type': 'text', 'id': 'direccion_editar', 'class': INPUT_CLASS}),
            'email': forms.TextInput(attrs={'type': 'text', 'id': 'email_editar', 'class': INPUT_CLASS}),
            'telefono': forms.TextInput(attrs={'type': 'text', 'id': 'telefono_editar', 'class': INPUT_CLASS}),
        }


class AddProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('producto', 'precio_unitario')
        labels = {
            'producto': 'Producto',
            'precio_unitario': 'Precio Unitario',
        }
        widgets = {
            'producto': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'precio_unitario': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
        }


class EditarProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('producto', 'precio_unitario')
        labels = {
            'producto': 'Producto',
            'precio_unitario': 'Precio Unitario',
        }
        widgets = {
            'producto': forms.TextInput(attrs={'type': 'text', 'id': 'producto_editar', 'class': INPUT_CLASS}),
            'precio_unitario': forms.NumberInput(attrs={'type': 'number', 'step': '0.01', 'id': 'precio_unitario_editar', 'class': INPUT_CLASS}),
        }


class EditarVentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ('id_cliente', 'fecha')
        labels = {
            'id_cliente': 'Cliente',
            'fecha': 'Fecha',
        }
        widgets = {
            'id_cliente': forms.Select(attrs={'class': INPUT_CLASS, 'id': 'id_cliente_editar'}),
            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': INPUT_CLASS, 'type': 'date', 'id': 'fecha_editar'},
            ),
        }


class AddVentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ('id_cliente', 'fecha')
        labels = {
            'id_cliente': 'Cliente',
            'fecha': 'Fecha',
        }
        widgets = {
            'id_cliente': forms.Select(attrs={'class': INPUT_CLASS, 'id': 'id_cliente_add'}),
            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': INPUT_CLASS, 'type': 'date', 'id': 'fecha_add', 'value': date.today()},
            ),
        }


class AddVentaDetalleForm(forms.ModelForm):

    class Meta:
        model = VentaDetalle
        fields = ('id_producto', 'cantidad', 'descuento')
        labels = {
            'id_producto': 'Producto',
            'cantidad': 'Cantidad',
            'descuento': 'Descuento',
        }
        widgets = {
            'id_producto': forms.Select(attrs={'class': INPUT_CLASS, 'id': 'id_producto_add'}),
            'cantidad': forms.NumberInput(attrs={'class': INPUT_CLASS, 'type': 'number', 'min': '1', 'id': 'cantidad_add'}),
            'descuento': forms.NumberInput(attrs={'class': INPUT_CLASS, 'type': 'number', 'step': '0.01', 'min': '0', 'id': 'descuento_add'}),
        }
