# Generated by Django 4.2.11 on 2024-11-07 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_tercero_options_remove_tercero_idtipotercero_and_more'),
        ('inventarios', '0024_kardex_despacho'),
    ]

    operations = [
        migrations.CreateModel(
            name='CierreInventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio', models.CharField(default='', max_length=4, verbose_name='Año')),
                ('cerrado', models.BooleanField(default=False, verbose_name='Cerrado')),
            ],
            options={
                'verbose_name': 'Cierre Inventario',
                'verbose_name_plural': 'Cierre Inventario',
                'ordering': ['anio'],
            },
        ),
        migrations.CreateModel(
            name='InventarioFisico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio', models.CharField(default='', max_length=4, verbose_name='Año')),
                ('inv_fis', models.IntegerField(default=0, verbose_name='Inv. Fisico')),
                ('inv_acum', models.IntegerField(default=0, verbose_name='Inventario')),
                ('IdBodega', models.ForeignKey(default=1, max_length=3, on_delete=django.db.models.deletion.CASCADE, related_name='inventario_fisico_bodega', to='inventarios.bodega', verbose_name='Acumulado Bodega')),
                ('IdItem', models.ForeignKey(default=1, max_length=3, on_delete=django.db.models.deletion.CASCADE, related_name='invntario_fisico_item', to='inventarios.maestroitem', verbose_name='Acumulado Items')),
                ('IdSucursal', models.ForeignKey(default=1, max_length=3, on_delete=django.db.models.deletion.CASCADE, related_name='inventario_fisico_sucursal', to='core.sucursal', verbose_name='Acumulado Sucursal')),
            ],
            options={
                'verbose_name': 'Inventario Físico',
                'verbose_name_plural': 'Inventario Físico',
                'ordering': ['IdItem'],
            },
        ),
    ]
