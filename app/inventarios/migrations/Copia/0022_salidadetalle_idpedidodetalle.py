# Generated by Django 4.2.11 on 2024-09-04 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarios', '0021_maestroitem_idbodega'),
    ]

    operations = [
        migrations.AddField(
            model_name='salidadetalle',
            name='IdPedidoDetalle',
            field=models.IntegerField(default=0, verbose_name='Id Pedido Detalle'),
        ),
    ]
