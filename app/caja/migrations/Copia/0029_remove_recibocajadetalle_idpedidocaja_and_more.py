# Generated by Django 4.2.11 on 2024-09-16 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0028_recibocajadetalle_idpedidocaja'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recibocajadetalle',
            name='IdPedidoCaja',
        ),
        migrations.AddField(
            model_name='recibocajadetalle',
            name='IdPedidoCajaDetalle',
            field=models.ForeignKey(default=1, max_length=10, on_delete=django.db.models.deletion.CASCADE, related_name='recibo_caja_detalle_pedido_caja', to='caja.pedidocajadetalle', verbose_name='Pedido Caja'),
        ),
    ]
