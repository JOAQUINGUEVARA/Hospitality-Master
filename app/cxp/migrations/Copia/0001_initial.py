# Generated by Django 4.2.11 on 2024-04-22 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacturaCompra',
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
                'verbose_name': 'Factura Compra',
                'verbose_name_plural': 'Facturas Compra',
                'ordering': ['numero'],
            },
        ),
        migrations.CreateModel(
            name='TipoDocumentoCxP',
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
            name='FacturaCompraDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('estado', models.BooleanField(default=False, verbose_name='Estado')),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor')),
                ('cantidad', models.IntegerField(default=0, verbose_name='Cantidad')),
                ('valor_total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor Total')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha de Edición')),
                ('IdFacturaCompra', models.ForeignKey(default=1, max_length=2, on_delete=django.db.models.deletion.CASCADE, related_name='factura_compra_detalle_despacho', to='cxp.facturacompra', verbose_name='Factura Compra')),
            ],
            options={
                'verbose_name': 'Detalle Factura Compra',
                'verbose_name_plural': 'Detalle Facturas Compra',
                'ordering': ['numero'],
            },
        ),
    ]
