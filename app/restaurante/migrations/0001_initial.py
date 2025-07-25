# Generated by Django 4.2.11 on 2025-06-27 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idMesa', models.CharField(blank=True, max_length=3, unique=True, verbose_name='Código Mesa')),
                ('descripcion', models.TextField(blank=True, default='', verbose_name='Descripción')),
                ('numero_sillas', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Número Sillas')),
                ('reserva', models.BooleanField(default=False, verbose_name='Reservada')),
                ('en_uso', models.BooleanField(default=False, verbose_name='En Uso')),
            ],
            options={
                'verbose_name': 'Mesa',
                'verbose_name_plural': 'Mesas',
                'ordering': ['descripcion'],
            },
        ),
        migrations.CreateModel(
            name='ReservaMesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(blank=True, default='', verbose_name='Descripción')),
                ('fecha_reserva', models.DateTimeField(default=None)),
                ('IdMesa', models.ForeignKey(default=1, max_length=2, on_delete=django.db.models.deletion.CASCADE, related_name='reserva_mesa', to='restaurante.mesa', verbose_name='Habitación')),
                ('IdSucursal', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reserva_mesa_sucursal', to='core.sucursal', verbose_name='Sucursal')),
                ('IdUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserva_mesa_usuario', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Reserva Mesa',
                'verbose_name_plural': 'Reservas Mesas',
                'ordering': ['descripcion'],
            },
        ),
    ]
