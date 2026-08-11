from django.db import migrations, models
import django.db.models.deletion


def poblar_codigos_curso(apps, schema_editor):
    Curso = apps.get_model('ventas', 'Curso')
    for curso in Curso.objects.all().order_by('id_producto'):
        Curso.objects.filter(pk=curso.pk).update(codigo=f'CURSO-{curso.id_producto}')


def poblar_precio_detalle(apps, schema_editor):
    VentaDetalle = apps.get_model('ventas', 'VentaDetalle')
    Curso = apps.get_model('ventas', 'Curso')
    cursos = {c.id_producto: c.precio_unitario for c in Curso.objects.all()}
    for detalle in VentaDetalle.objects.all():
        if detalle.precio_unitario is None:
            precio = cursos.get(detalle.id_producto_id)
            if precio is not None:
                VentaDetalle.objects.filter(pk=detalle.pk).update(precio_unitario=precio)


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Producto',
            new_name='Curso',
        ),
        migrations.AddField(
            model_name='curso',
            name='codigo',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='descripcion',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='curso',
            name='duracion_horas',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='curso',
            name='modalidad',
            field=models.CharField(
                choices=[('presencial', 'Presencial'), ('online', 'En linea'), ('hibrido', 'Hibrido')],
                default='online',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='curso',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(poblar_codigos_curso, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='curso',
            name='codigo',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameField(
                    model_name='curso',
                    old_name='id_producto',
                    new_name='id_curso',
                ),
                migrations.RenameField(
                    model_name='curso',
                    old_name='producto',
                    new_name='nombre',
                ),
                migrations.RenameField(
                    model_name='curso',
                    old_name='precio_unitario',
                    new_name='precio_lista',
                ),
                migrations.AlterField(
                    model_name='curso',
                    name='id_curso',
                    field=models.AutoField(db_column='id_producto', primary_key=True, serialize=False),
                ),
                migrations.AlterField(
                    model_name='curso',
                    name='nombre',
                    field=models.CharField(db_column='producto', max_length=120),
                ),
                migrations.AlterField(
                    model_name='curso',
                    name='precio_lista',
                    field=models.DecimalField(db_column='precio_unitario', decimal_places=4, max_digits=19),
                ),
            ],
            database_operations=[
                migrations.AlterField(
                    model_name='curso',
                    name='producto',
                    field=models.CharField(max_length=120),
                ),
            ],
        ),
        migrations.AlterField(
            model_name='cliente',
            name='direccion',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AddField(
            model_name='cliente',
            name='curp',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='empresa',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id_vendedor', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'cat_vendedor',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='venta',
            name='estado',
            field=models.CharField(
                choices=[('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')],
                default='confirmada',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='venta',
            name='observaciones',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='venta',
            name='registrado_en',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='venta',
            name='id_vendedor',
            field=models.ForeignKey(
                blank=True,
                db_column='id_vendedor',
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name='ventas',
                to='ventas.vendedor',
            ),
        ),
        migrations.AddField(
            model_name='ventadetalle',
            name='precio_unitario',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True),
        ),
        migrations.RunPython(poblar_precio_detalle, migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameField(
                    model_name='ventadetalle',
                    old_name='id_producto',
                    new_name='id_curso',
                ),
                migrations.AlterField(
                    model_name='ventadetalle',
                    name='id_curso',
                    field=models.ForeignKey(
                        db_column='id_producto',
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to='ventas.curso',
                    ),
                ),
                migrations.AlterUniqueTogether(
                    name='ventadetalle',
                    unique_together={('id_venta', 'id_curso')},
                ),
            ],
            database_operations=[],
        ),
        migrations.AlterField(
            model_name='ventadetalle',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
    ]
