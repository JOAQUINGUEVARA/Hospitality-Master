# Generated by Django 4.2.11 on 2024-08-08 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0006_detalledespacho_despacho_alter_despacho_idproveedor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detalledespacho',
            old_name='despacho',
            new_name='IdDespacho',
        ),
    ]
