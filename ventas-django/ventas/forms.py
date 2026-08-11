from datetime import date

from django import forms

from ventas.models import Cliente, Curso, Venta, VentaDetalle

INPUT = 'form-control'
SELECT = 'form-select'


class AddClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ('nombre', 'apellidos', 'direccion', 'email', 'telefono', 'curp', 'empresa')
        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'direccion': 'Direccion',
            'email': 'Correo electronico',
            'telefono': 'Telefono',
            'curp': 'CURP',
            'empresa': 'Empresa',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': INPUT}),
            'apellidos': forms.TextInput(attrs={'class': INPUT}),
            'direccion': forms.TextInput(attrs={'class': INPUT}),
            'email': forms.EmailInput(attrs={'class': INPUT}),
            'telefono': forms.TextInput(attrs={'class': INPUT}),
            'curp': forms.TextInput(attrs={'class': INPUT}),
            'empresa': forms.TextInput(attrs={'class': INPUT}),
        }


class EditarClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = AddClienteForm.Meta.fields
        labels = AddClienteForm.Meta.labels
        widgets = {
            'nombre': forms.TextInput(attrs={'class': INPUT, 'id': 'nombre_editar'}),
            'apellidos': forms.TextInput(attrs={'class': INPUT, 'id': 'apellidos_editar'}),
            'direccion': forms.TextInput(attrs={'class': INPUT, 'id': 'direccion_editar'}),
            'email': forms.EmailInput(attrs={'class': INPUT, 'id': 'email_editar'}),
            'telefono': forms.TextInput(attrs={'class': INPUT, 'id': 'telefono_editar'}),
            'curp': forms.TextInput(attrs={'class': INPUT, 'id': 'curp_editar'}),
            'empresa': forms.TextInput(attrs={'class': INPUT, 'id': 'empresa_editar'}),
        }


class AddCursoForm(forms.ModelForm):

    class Meta:
        model = Curso
        fields = ('codigo', 'nombre', 'descripcion', 'duracion_horas', 'modalidad', 'precio_lista', 'activo')
        labels = {
            'codigo': 'Codigo',
            'nombre': 'Nombre del curso',
            'descripcion': 'Descripcion',
            'duracion_horas': 'Duracion (horas)',
            'modalidad': 'Modalidad',
            'precio_lista': 'Precio de lista',
            'activo': 'Activo',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'PY-101'}),
            'nombre': forms.TextInput(attrs={'class': INPUT}),
            'descripcion': forms.Textarea(attrs={'class': INPUT, 'rows': 3}),
            'duracion_horas': forms.NumberInput(attrs={'class': INPUT, 'min': '1'}),
            'modalidad': forms.Select(attrs={'class': SELECT}),
            'precio_lista': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'min': '0'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EditarCursoForm(forms.ModelForm):

    class Meta:
        model = Curso
        fields = AddCursoForm.Meta.fields
        labels = AddCursoForm.Meta.labels
        widgets = {
            'codigo': forms.TextInput(attrs={'class': INPUT, 'id': 'codigo_editar'}),
            'nombre': forms.TextInput(attrs={'class': INPUT, 'id': 'nombre_editar'}),
            'descripcion': forms.Textarea(attrs={'class': INPUT, 'rows': 3, 'id': 'descripcion_editar'}),
            'duracion_horas': forms.NumberInput(attrs={'class': INPUT, 'id': 'duracion_horas_editar'}),
            'modalidad': forms.Select(attrs={'class': SELECT, 'id': 'modalidad_editar'}),
            'precio_lista': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'id': 'precio_lista_editar'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'activo_editar'}),
        }


class EditarVentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ('id_cliente', 'fecha', 'estado', 'observaciones')
        labels = {
            'id_cliente': 'Cliente',
            'fecha': 'Fecha',
            'estado': 'Estado',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'id_cliente': forms.Select(attrs={'class': SELECT, 'id': 'id_cliente_editar'}),
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'class': INPUT, 'type': 'date', 'id': 'fecha_editar'}),
            'estado': forms.Select(attrs={'class': SELECT, 'id': 'estado_editar'}),
            'observaciones': forms.Textarea(attrs={'class': INPUT, 'rows': 2, 'id': 'observaciones_editar'}),
        }


class AddVentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ('id_cliente', 'fecha', 'observaciones')
        labels = {
            'id_cliente': 'Cliente',
            'fecha': 'Fecha de venta',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'id_cliente': forms.Select(attrs={'class': SELECT, 'id': 'id_cliente_add'}),
            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': INPUT, 'type': 'date', 'id': 'fecha_add', 'value': date.today().isoformat()},
            ),
            'observaciones': forms.Textarea(attrs={'class': INPUT, 'rows': 2, 'id': 'observaciones_add'}),
        }


class AddVentaDetalleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_curso'].queryset = Curso.objects.filter(activo=True).order_by('nombre')
        self.fields['cantidad'].initial = 1

    class Meta:
        model = VentaDetalle
        fields = ('id_curso', 'cantidad', 'descuento')
        labels = {
            'id_curso': 'Curso',
            'cantidad': 'Plazas',
            'descuento': 'Descuento ($)',
        }
        widgets = {
            'id_curso': forms.Select(attrs={'class': SELECT, 'id': 'id_curso_add'}),
            'cantidad': forms.NumberInput(attrs={'class': INPUT, 'min': '1', 'id': 'cantidad_add', 'value': '1'}),
            'descuento': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'min': '0', 'id': 'descuento_add'}),
        }


# Alias legacy
AddProductoForm = AddCursoForm
EditarProductoForm = EditarCursoForm
