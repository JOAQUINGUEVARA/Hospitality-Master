# Generated by Django 4.2.11 on 2024-08-05 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarios', '0016_remove_proveedoritem_idfacturacompra'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='despacho',
            field=models.CharField(default='', max_length=15, verbose_name='Despacho'),
        ),
    ]
