from django.db import models

from hotel.models import Habitacion
from core.models import Sucursal
from django.contrib.auth.models import User

class Mesa(models.Model):
    idMesa = models.CharField(max_length=3,blank=True,unique=True,verbose_name='Código Mesa')
    descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
    numero_sillas = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Número Sillas')
    reserva = models.BooleanField(default=False,verbose_name='Reservada')
    en_uso = models.BooleanField(default=False,verbose_name='En Uso')

    class Meta:
        ordering=["descripcion"]
        verbose_name='Mesa'
        verbose_name_plural='Mesas'

    def __str__(self):
        return self.idMesa+'-'+self.descripcion
    
class ReservaMesa(models.Model):
    #idMesa = models.CharField(max_length=3,blank=True,verbose_name='Código Mesa')
    IdMesa = models.ForeignKey(Mesa,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Habitación',related_name='reserva_mesa')
    descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
    fecha_reserva = models.DateTimeField(default=None)
    IdSucursal = models.ForeignKey(Sucursal,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name="reserva_mesa_sucursal")
    IdUsuario = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Usuario',related_name="reserva_mesa_usuario")
    
    class Meta:
        ordering=["descripcion"]
        verbose_name='Reserva Mesa'
        verbose_name_plural='Reservas Mesas'

    def __str__(self):
        return self.idMesa+'-'+self.descripcion    