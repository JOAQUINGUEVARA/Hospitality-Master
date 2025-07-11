# Generated by Django 4.2.11 on 2024-11-21 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_mes_options_rename_mes_mes_idmes_and_more'),
        ('inventarios', '0032_remove_inventariofisico_anio_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AjusteInventarioFisico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IdAnio', models.ForeignKey(default=1, max_length=2, on_delete=django.db.models.deletion.CASCADE, related_name='ajuste_inventario_fisico_anio', to='core.anio', verbose_name='Año')),
                ('IdBodega', models.ForeignKey(default=1, max_length=3, on_delete=django.db.models.deletion.CASCADE, related_name='ajuste_bodega', to='inventarios.bodega', verbose_name='Bodega')),
                ('IdMes', models.ForeignKey(default=1, max_length=2, on_delete=django.db.models.deletion.CASCADE, related_name='ajuste_inventario_fisico_mes', to='core.mes', verbose_name='Mes')),
                ('IdSucursal', models.ForeignKey(default=1, max_length=2, on_delete=django.db.models.deletion.CASCADE, related_name='ajuste_sucursal', to='core.sucursal', verbose_name='Sucursal')),
            ],
            options={
                'verbose_name': 'Ajuste',
                'verbose_name_plural': 'Ajustes',
                'ordering': ['IdAnio'],
            },
        ),
        migrations.DeleteModel(
            name='Ajuste',
        ),
    ]
