# Generated by Django 4.2.11 on 2024-11-19 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_anio_mes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mes',
            options={'ordering': ['idMes'], 'verbose_name': 'Mes', 'verbose_name_plural': 'Meses'},
        ),
        migrations.RenameField(
            model_name='mes',
            old_name='mes',
            new_name='idMes',
        ),
        migrations.AlterField(
            model_name='mes',
            name='descripcion',
            field=models.CharField(default='', max_length=15, verbose_name='Mes'),
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='descripcion',
            field=models.TextField(blank=True, default='', verbose_name='Sucursal'),
        ),
    ]
