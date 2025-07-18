# Generated by Django 4.2.11 on 2024-08-23 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_tercero_options_remove_tercero_idtipotercero_and_more'),
        ('inventarios', '0019_alter_entrada_idproveedor_kardex'),
    ]

    operations = [
        migrations.AddField(
            model_name='kardex',
            name='IdBodega',
            field=models.ForeignKey(default=1, max_length=3, on_delete=django.db.models.deletion.CASCADE, related_name='kardex_bodega', to='inventarios.bodega', verbose_name='Bodega'),
        ),
        migrations.AddField(
            model_name='kardex',
            name='IdSucursal',
            field=models.ForeignKey(default=1, max_length=2, on_delete=django.db.models.deletion.CASCADE, related_name='kardex_sucursal', to='core.sucursal', verbose_name='Sucursal'),
        ),
        migrations.AlterField(
            model_name='kardex',
            name='saldo',
            field=models.IntegerField(default=0, verbose_name='Saldo'),
        ),
    ]
