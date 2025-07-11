from django.db import models
from core.models import Sucursal,Tercero,TipoIdentificacion
from django.contrib.auth.models import User
# Create your models here.


class TipoHabitacion(models.Model):
    idTipoHabitacion = models.CharField(max_length=3,blank=True,unique=True,verbose_name='Código Tipo Habitación')
    descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
    #imagen_Tipo_habitacion=models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,default='0.jpeg')

    class Meta:
        ordering=["descripcion"]
        verbose_name='Tipo Habitación'
        verbose_name_plural='Tipos Habitaciones'

    def __str__(self):
        return self.descripcion
	
class Habitacion(models.Model):
    idHabitacion = models.CharField(max_length=3,blank=True,unique=True,verbose_name='Código Habitación')
    IdTipoHabitacion = models.ForeignKey(TipoHabitacion,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Habitación',related_name='habitacion_tipo_habitacion')  
    descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
    valor_noche = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Noche')
    ocupada = models.BooleanField(default=False,verbose_name='Ocupada')
    
    class Meta:
        ordering=["descripcion"]
        verbose_name='Habitación'
        verbose_name_plural='Habitaciones'

    def __str__(self):
        return self.idHabitacion+'-'+self.descripcion

class RegistroHotel(models.Model):
    MOTIVO_VIAJE = (
		('1','Recreación'),
		('2','Negocios'),
		('3','Salud'),
		('4','Otros'),
		)
    EQUIPAJE =(
        ('Si','Si'),
		('No','No'),
    )
    consecutivo = models.CharField(max_length=15,default='',verbose_name='Consecutivo',unique=True)
    IdHabitacion = models.ForeignKey(Habitacion,max_length=2,null=False,blank=False,on_delete=models.CASCADE,verbose_name='Habitación',related_name='registro_habitacion')
    IdTercero = models.ForeignKey(Tercero,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Cliente:',related_name='registro_tercero')
    descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
    tarifa_habitacion = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Tarifa Habitación')
    check_in = models.DateField(default=None,null=True,verbose_name='Registro Entrada (Check In)')
    hora_check_in = models.TimeField(auto_now_add=False,null=True,auto_now=True,verbose_name='Hora Registro Entrada')
    check_out = models.DateField(default=None,null=True,verbose_name='Registro Salida (check Out)')
    hora_check_out = models.TimeField(default=None,null=True,verbose_name='Hora Registro Salida')
    no_de_dias=models.IntegerField(default=0,verbose_name='Nro. Días')
    no_de_noches=models.IntegerField(default=0,verbose_name='Nro. Noches')
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Pago')
    ocupacion = models.CharField(default='',max_length=100,verbose_name='Ocupación')
    empresa = models.CharField(default='',max_length=100,verbose_name='Empresa')
    nacionalidad = models.CharField(default='',max_length=100,verbose_name='Nacionalidad')
    motivo_viaje = models.CharField(default='1',max_length=1,choices=MOTIVO_VIAJE,verbose_name='Motivo Viaje')
    procedencia = models.CharField(default='',max_length=100,verbose_name='Procedencia')
    destino = models.CharField(default='',max_length=100,verbose_name='Destino')
    placa_vehiculo = models.CharField(default='',max_length=10,verbose_name='Placa Vehículo')
    dias_estadia = models.IntegerField(default=0,verbose_name='Días Estadía')
    no_adultos = models.IntegerField(default=0,verbose_name='No. Adultos')
    no_ninos = models.IntegerField(default=0,verbose_name='No. Niños')
    equipaje = models.CharField(default='No',max_length=2,choices=EQUIPAJE,verbose_name='Equipaje')
    consec_reserva = models.CharField(max_length=15,default='',verbose_name='Consec. Reserva')
    pagado = models.BooleanField(default=False,verbose_name='Pagado')
    no_recibo_caja = models.CharField(default='',max_length=10,verbose_name='Recibo Caja')   
    class Meta:
        ordering=["descripcion"]
        verbose_name='Registro Hotel'
        verbose_name_plural='Registro Hotel'

    def __str__(self):
        return self.IdHabitacion.descripcion

class AcompañanteHotel(models.Model):
    IdRegistro = models.ForeignKey(RegistroHotel,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='RegistroHotel',related_name='acompañante_registro_hotel')
    identificacion= models.CharField(max_length=15,null=True,blank=True,default='',verbose_name='Nro. Identificación')
    IdTipoIdentificacion=models.ForeignKey(TipoIdentificacion,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo de Indetificación',related_name='acompañante_tipoidentificacion')
    identifica_de = models.CharField(default='',max_length=100,verbose_name='Identificacion de')
    apenom = models.CharField(max_length=80,default='',verbose_name='Nombre')
    lugar_residencia = models.CharField(max_length=80,default='',verbose_name='Lugar Residencia')	

    class Meta:
        ordering=['identificacion']
        verbose_name='Acompañante'
        verbose_name_plural='Acompañantes'
              	
class ReservaHabitacion(models.Model):
    IdHabitacion = models.ForeignKey(Habitacion,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Habitación',related_name='reserva_habitacion')  
    consecutivo = models.CharField(max_length=15,default='',unique=True,verbose_name='Consecutivo')
    descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
    fecha_ingreso = models.DateField(default=None,verbose_name='Fecha Entrada')
    fecha_salida = models.DateField(default=None,verbose_name='Fecha Salida')
    fecha_reserva = models.DateField(default=None,verbose_name='Fecha Reserva')
    valor_reserva = models.FloatField(default=0,verbose_name='Valor Reserva')
    telefono=models.CharField(max_length=50,default='',verbose_name='Teléfono')
    nombre_reserva=models.CharField(max_length=60,default='',verbose_name='Nombre Reserva')
    email=models.CharField(max_length=100,default='',verbose_name='Email')
    pin=models.IntegerField(default=0,verbose_name='Pin')
    no_de_dias=models.IntegerField(default=0,verbose_name='Nro. Días')
    no_de_noches=models.IntegerField(default=0,verbose_name='Nro. Noches')
    IdSucursal = models.ForeignKey(Sucursal,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name="reserva_habitacion_sucursal")
    IdUsuario = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Usuario',related_name="reserva_habitacion_usuario")

    class Meta:
        ordering=["descripcion"]
        verbose_name='Reserva Habitación'
        verbose_name_plural='Reservas Habitaciones'

    def __str__(self):
        return "ID. Reserva: "+str(self.consecutivo)

