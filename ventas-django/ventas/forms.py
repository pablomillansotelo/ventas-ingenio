from datetime import date

from django import forms

from ventas.models import (
    Cliente,
    Curso,
    EdicionCurso,
    Inscripcion,
    Pago,
    Vendedor,
    Venta,
    VentaDetalle,
)

INPUT = 'form-control'
SELECT = 'form-select'


class AddClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = (
            'nombre', 'apellidos', 'direccion', 'email', 'telefono',
            'curp', 'empresa', 'notas', 'activo',
        )
        labels = {
            'nombre': 'Nombre',
            'apellidos': 'Apellidos',
            'direccion': 'Dirección',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'curp': 'CURP',
            'empresa': 'Empresa',
            'notas': 'Notas',
            'activo': 'Activo',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Apellidos'}),
            'direccion': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'Dirección'}),
            'email': forms.EmailInput(attrs={'class': INPUT, 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': INPUT, 'placeholder': '5551234567'}),
            'curp': forms.TextInput(attrs={'class': INPUT}),
            'empresa': forms.TextInput(attrs={'class': INPUT}),
            'notas': forms.Textarea(attrs={'class': INPUT, 'rows': 2}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
            'notas': forms.Textarea(attrs={'class': INPUT, 'rows': 2, 'id': 'notas_editar'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'activo_cliente_editar'}),
        }


class AddVendedorForm(forms.ModelForm):

    class Meta:
        model = Vendedor
        fields = ('user_id', 'nombre', 'email', 'telefono', 'comision_pct', 'activo')
        labels = {
            'user_id': 'ID usuario (auth)',
            'nombre': 'Nombre',
            'email': 'Correo',
            'telefono': 'Teléfono',
            'comision_pct': 'Comisión (%)',
            'activo': 'Activo',
        }
        widgets = {
            'user_id': forms.NumberInput(attrs={'class': INPUT}),
            'nombre': forms.TextInput(attrs={'class': INPUT}),
            'email': forms.EmailInput(attrs={'class': INPUT}),
            'telefono': forms.TextInput(attrs={'class': INPUT}),
            'comision_pct': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'min': '0'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EditarVendedorForm(forms.ModelForm):

    class Meta:
        model = Vendedor
        fields = AddVendedorForm.Meta.fields
        labels = AddVendedorForm.Meta.labels
        widgets = {
            'user_id': forms.NumberInput(attrs={'class': INPUT, 'id': 'user_id_editar'}),
            'nombre': forms.TextInput(attrs={'class': INPUT, 'id': 'nombre_vendedor_editar'}),
            'email': forms.EmailInput(attrs={'class': INPUT, 'id': 'email_vendedor_editar'}),
            'telefono': forms.TextInput(attrs={'class': INPUT, 'id': 'telefono_vendedor_editar'}),
            'comision_pct': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'id': 'comision_editar'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'activo_vendedor_editar'}),
        }


class AddCursoForm(forms.ModelForm):

    class Meta:
        model = Curso
        fields = ('codigo', 'nombre', 'descripcion', 'duracion_horas', 'modalidad', 'precio_lista', 'activo')
        labels = {
            'codigo': 'Código',
            'nombre': 'Nombre del curso',
            'descripcion': 'Descripción',
            'duracion_horas': 'Duración (horas)',
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
            'nombre': forms.TextInput(attrs={'class': INPUT, 'id': 'nombre_curso_editar'}),
            'descripcion': forms.Textarea(attrs={'class': INPUT, 'rows': 3, 'id': 'descripcion_editar'}),
            'duracion_horas': forms.NumberInput(attrs={'class': INPUT, 'id': 'duracion_horas_editar'}),
            'modalidad': forms.Select(attrs={'class': SELECT, 'id': 'modalidad_editar'}),
            'precio_lista': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'id': 'precio_lista_editar'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'activo_editar'}),
        }


class AddEdicionForm(forms.ModelForm):

    class Meta:
        model = EdicionCurso
        fields = (
            'id_curso', 'codigo_edicion', 'fecha_inicio', 'fecha_fin',
            'cupo_maximo', 'precio_edicion', 'estado', 'activo',
        )
        labels = {
            'id_curso': 'Curso',
            'codigo_edicion': 'Código edición',
            'fecha_inicio': 'Fecha inicio',
            'fecha_fin': 'Fecha fin',
            'cupo_maximo': 'Cupo máximo',
            'precio_edicion': 'Precio edición (opcional)',
            'estado': 'Estado',
            'activo': 'Activa',
        }
        widgets = {
            'id_curso': forms.Select(attrs={'class': SELECT}),
            'codigo_edicion': forms.TextInput(attrs={'class': INPUT, 'placeholder': 'PY-101-2026-01'}),
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'class': INPUT, 'type': 'date'}),
            'fecha_fin': forms.DateInput(format='%Y-%m-%d', attrs={'class': INPUT, 'type': 'date'}),
            'cupo_maximo': forms.NumberInput(attrs={'class': INPUT, 'min': '1'}),
            'precio_edicion': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'min': '0'}),
            'estado': forms.Select(attrs={'class': SELECT}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EditarEdicionForm(forms.ModelForm):

    class Meta:
        model = EdicionCurso
        fields = AddEdicionForm.Meta.fields
        labels = AddEdicionForm.Meta.labels
        widgets = {
            'id_curso': forms.Select(attrs={'class': SELECT, 'id': 'id_curso_edicion_editar'}),
            'codigo_edicion': forms.TextInput(attrs={'class': INPUT, 'id': 'codigo_edicion_editar'}),
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d', attrs={'class': INPUT, 'type': 'date', 'id': 'fecha_inicio_editar'}),
            'fecha_fin': forms.DateInput(format='%Y-%m-%d', attrs={'class': INPUT, 'type': 'date', 'id': 'fecha_fin_editar'}),
            'cupo_maximo': forms.NumberInput(attrs={'class': INPUT, 'id': 'cupo_maximo_editar'}),
            'precio_edicion': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'id': 'precio_edicion_editar'}),
            'estado': forms.Select(attrs={'class': SELECT, 'id': 'estado_edicion_editar'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'activo_edicion_editar'}),
        }


class EditarVentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ('id_cliente', 'fecha', 'estado', 'estado_pago', 'observaciones')
        labels = {
            'id_cliente': 'Cliente',
            'fecha': 'Fecha de venta',
            'estado': 'Estado venta',
            'estado_pago': 'Estado de pago',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'id_cliente': forms.Select(attrs={'class': SELECT, 'id': 'id_cliente_editar'}),
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'class': INPUT, 'type': 'date', 'id': 'fecha_editar'}),
            'estado': forms.Select(attrs={'class': SELECT, 'id': 'estado_editar'}),
            'estado_pago': forms.Select(attrs={'class': SELECT, 'id': 'estado_pago_editar'}),
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
        self.fields['id_edicion'].queryset = EdicionCurso.objects.filter(
            activo=True,
            estado__in=[EdicionCurso.ESTADO_PROGRAMADA, EdicionCurso.ESTADO_EN_CURSO],
        ).select_related('id_curso').order_by('codigo_edicion')
        self.fields['id_edicion'].required = False
        self.fields['id_edicion'].label_from_instance = (
            lambda obj: f'[{obj.id_curso_id}] {obj.codigo_edicion} ({obj.cupo_disponible} lugares)'
        )
        self.fields['cantidad'].initial = 1

    class Meta:
        model = VentaDetalle
        fields = ('id_curso', 'id_edicion', 'cantidad', 'descuento')
        labels = {
            'id_curso': 'Curso',
            'id_edicion': 'Edición (opcional)',
            'cantidad': 'Plazas',
            'descuento': 'Descuento ($)',
        }
        widgets = {
            'id_curso': forms.Select(attrs={'class': SELECT, 'id': 'id_curso_add'}),
            'id_edicion': forms.Select(attrs={'class': SELECT, 'id': 'id_edicion_add'}),
            'cantidad': forms.NumberInput(attrs={'class': INPUT, 'min': '1', 'id': 'cantidad_add', 'value': '1'}),
            'descuento': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'min': '0', 'id': 'descuento_add', 'placeholder': '0.00'}),
        }


class AddPagoForm(forms.ModelForm):

    class Meta:
        model = Pago
        fields = ('id_venta', 'monto', 'metodo', 'referencia', 'fecha_pago', 'estado')
        labels = {
            'id_venta': 'Venta',
            'monto': 'Monto',
            'metodo': 'Método de pago',
            'referencia': 'Referencia / folio',
            'fecha_pago': 'Fecha de pago',
            'estado': 'Estado',
        }
        widgets = {
            'id_venta': forms.Select(attrs={'class': SELECT}),
            'monto': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'min': '0.01'}),
            'metodo': forms.Select(attrs={'class': SELECT}),
            'referencia': forms.TextInput(attrs={'class': INPUT}),
            'fecha_pago': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'class': INPUT, 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': SELECT}),
        }


class EditarPagoForm(forms.ModelForm):

    class Meta:
        model = Pago
        fields = AddPagoForm.Meta.fields
        labels = AddPagoForm.Meta.labels
        widgets = {
            'id_venta': forms.Select(attrs={'class': SELECT, 'id': 'id_venta_pago_editar'}),
            'monto': forms.NumberInput(attrs={'class': INPUT, 'step': '0.01', 'id': 'monto_pago_editar'}),
            'metodo': forms.Select(attrs={'class': SELECT, 'id': 'metodo_pago_editar'}),
            'referencia': forms.TextInput(attrs={'class': INPUT, 'id': 'referencia_pago_editar'}),
            'fecha_pago': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'class': INPUT, 'type': 'datetime-local', 'id': 'fecha_pago_editar'}),
            'estado': forms.Select(attrs={'class': SELECT, 'id': 'estado_pago_reg_editar'}),
        }


class AddInscripcionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_edicion'].required = False

    class Meta:
        model = Inscripcion
        fields = ('id_cliente', 'id_curso', 'id_edicion', 'estado')
        labels = {
            'id_cliente': 'Cliente',
            'id_curso': 'Curso',
            'id_edicion': 'Edición',
            'estado': 'Estado',
        }
        widgets = {
            'id_cliente': forms.Select(attrs={'class': SELECT}),
            'id_curso': forms.Select(attrs={'class': SELECT}),
            'id_edicion': forms.Select(attrs={'class': SELECT}),
            'estado': forms.Select(attrs={'class': SELECT}),
        }


class EditarInscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion
        fields = ('estado',)
        labels = {'estado': 'Estado'}
        widgets = {
            'estado': forms.Select(attrs={'class': SELECT, 'id': 'estado_inscripcion_editar'}),
        }


AddProductoForm = AddCursoForm
EditarProductoForm = EditarCursoForm
