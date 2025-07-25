# Generated by Django 4.2.11 on 2024-04-25 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=80, verbose_name='Nombre Empresa')),
                ('nit', models.CharField(max_length=15, verbose_name='Nit Empresa')),
                ('direccion', models.CharField(max_length=50, verbose_name='Dirección Empresa')),
                ('telefonos', models.CharField(max_length=50, verbose_name='Teléfono Empresa')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
                'ordering': ['nombre'],
            },
        ),
    ]
