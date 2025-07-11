# Generated by Django 4.2.11 on 2024-04-22 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idCaja', models.CharField(blank=True, default='', max_length=2, verbose_name='Código Caja')),
                ('valor_base', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor Base')),
                ('ingresos', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Ingresos')),
                ('egresos', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Egresos')),
                ('descripcion', models.TextField(blank=True, default='', verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Forma de Pago',
                'verbose_name_plural': 'Formas de Pago',
                'ordering': ['descripcion'],
            },
        ),
        migrations.CreateModel(
            name='EgresoCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('fecha', models.DateField(blank=True, null=True, verbose_name='Fecha')),
                ('detalle', models.TextField(blank=True, default='', verbose_name='Detalle')),
                ('estado', models.BooleanField(default=False, verbose_name='Estado')),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de Edición')),
            ],
            options={
                'verbose_name': 'Egreso Caja',
                'verbose_name_plural': 'Egreso Caja',
                'ordering': ['numero'],
            },
        ),
        migrations.CreateModel(
            name='ReciboCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('fecha', models.DateField(blank=True, null=True, verbose_name='Fecha')),
                ('detalle', models.TextField(blank=True, default='', verbose_name='Detalle')),
                ('estado', models.BooleanField(default=False, verbose_name='Estado')),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de Edición')),
            ],
            options={
                'verbose_name': 'Recibo Caja',
                'verbose_name_plural': 'Recibos Caja',
                'ordering': ['numero'],
            },
        ),
        migrations.CreateModel(
            name='ReciboCajaDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor')),
                ('cantidad', models.IntegerField(default=0, verbose_name='Cantidad')),
                ('valor_total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor Total')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de Edición')),
            ],
            options={
                'verbose_name': 'Detalle Recibo Caja',
                'verbose_name_plural': 'Detalle Recibos Caja',
                'ordering': ['numero'],
            },
        ),
        migrations.CreateModel(
            name='TipoDocumentoCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idTipo', models.CharField(blank=True, max_length=3, verbose_name='Código Tipo Documento')),
                ('descripcion', models.TextField(blank=True, default='', verbose_name='Descripción')),
                ('numeracion', models.BooleanField(default=False, verbose_name='Numeración')),
                ('caracteres', models.CharField(max_length=3, verbose_name='Caracteres')),
                ('longitud', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Longitud')),
                ('actual', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Actual')),
            ],
            options={
                'verbose_name': 'Tipo Documento',
                'verbose_name_plural': 'Tipos Documento',
                'ordering': ['descripcion'],
            },
        ),
        migrations.CreateModel(
            name='TipoEgresoCaja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idTipoEgreso', models.CharField(blank=True, default='', max_length=2, verbose_name='Código Tipo Egreso')),
                ('descripcion', models.TextField(blank=True, default='', verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Tipo de Egreso',
                'verbose_name_plural': 'Tipos de Egreso',
                'ordering': ['descripcion'],
            },
        ),
    ]
