# Generated by Django 4.2.11 on 2024-05-15 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0015_alter_pedidocaja_options_pedidocaja_valor_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidocaja',
            name='total_items',
            field=models.IntegerField(default=0, verbose_name='Total Items'),
        ),
    ]
