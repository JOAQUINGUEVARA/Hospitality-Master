# Generated by Django 4.2.11 on 2024-07-03 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarios', '0011_alter_maestroitem_tipo_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='acumuladoitem',
            name='cant_maxima',
            field=models.IntegerField(default=0, verbose_name='Cantidad Máxima'),
        ),
        migrations.AddField(
            model_name='acumuladoitem',
            name='cant_minima',
            field=models.IntegerField(default=0, verbose_name='Cantidad Mínima'),
        ),
        migrations.AddField(
            model_name='acumuladoitem',
            name='costo_prom',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Costo Promedio'),
        ),
    ]
