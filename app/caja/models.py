from django.db import models

# Create your models here.

from datetime import date
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum

from core.models import Sucursal,Tercero
from tesoreria.models import Banco
from inventarios.models import MaestroItem
from restaurante.models import Mesa
from hotel.models import Habitacion

class TipoDocumentoCaja(models.Model):
	idTipo = models.CharField(max_length=3,unique=True,verbose_name='Código Tipo Documento')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	numeracion=models.BooleanField(default=False,verbose_name='Numeración') #numeracion
	caracteres=models.CharField(max_length=3,null=False,blank=False,verbose_name='Caracteres')
	longitud=models.PositiveIntegerField(null=True,blank=True,default=0,verbose_name='Longitud') 
	actual=models.PositiveIntegerField(null=True,blank=True,default=0,verbose_name='Actual')

	class Meta:
		ordering=["descripcion"]
		verbose_name='Tipo Documento'
		verbose_name_plural='Tipos Documento'

	def __str__(self):
		return self.descripcion
	
class Caja(models.Model):
	idCaja=models.CharField(max_length=2,unique=True,verbose_name='Código Caja')
	valor_base = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Base')
	ingresos = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Ingresos')
	egresos = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Egresos')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	consolidada = models.BooleanField(default=False,verbose_name='Consolidada')   

	class Meta:
		ordering=["descripcion"]
		verbose_name='Caja'
		verbose_name_plural='Cajas'

	def __str__(self):
		return self.descripcion

class TipoEgresoCaja(models.Model):
	idTipoEgreso=models.CharField(max_length=2,unique=True,verbose_name='Código Tipo Egreso')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')    

	class Meta:
		ordering=["descripcion"]
		verbose_name='Tipo de Egreso'
		verbose_name_plural='Tipos de Egreso'

	def __str__(self):
		return self.descripcion

class TipoIngresoCaja(models.Model):
	idTipoIngreso=models.CharField(max_length=2,unique=True,verbose_name='Código Tipo Ingreso')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')    

	class Meta:
		ordering=["descripcion"]
		verbose_name='Tipo de Ingreso Caja'
		verbose_name_plural='Tipos de Ingreso Caja'

	def __str__(self):
		return self.descripcion
	
class EgresoCaja(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCaja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='egreso_caja_tipodocumento')
	IdTipoEgreso = models.ForeignKey(TipoEgresoCaja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='egreso_caja_tipodocumento')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	IdCaja = models.ForeignKey(Caja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Caja No.',related_name='egreso_caja_caja')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='egreso_caja_sucursal')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='egreso_caja_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Egreso Caja'
		verbose_name_plural='Egresos Caja'

	def __str__(self):
		return self.IdTipoDocumento.descripcion+'-'+self.numero		
	
class PedidoCaja(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCaja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='pedido_caja_tipodocumento')
	IdTipoIngreso = models.ForeignKey(TipoIngresoCaja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Ingreso',related_name='pedido_caja_tipoingreso')
	IdCaja = models.ForeignKey(Caja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Caja',related_name='pedido_caja')
	IdMesa = models.ForeignKey(Mesa,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Mesa',related_name='pedido_caja_mesa')
	IdHabitacion = models.ForeignKey(Habitacion,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Habitacion',related_name='pedido_caja_habitacion')
	recibo_caja = models.CharField(max_length=10,default='',verbose_name='Recibo Caja')
	total_items = models.IntegerField(default=0,verbose_name='Total Items')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Total')
	IdSucursal = models.ForeignKey(Sucursal,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name="pedido_caja_sucursal")	# SUCURSAL
	IdUsuario = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Usuario',related_name="pedido_caja_usuario") # USUARIO
	cerrado = models.BooleanField(default=False,verbose_name='Cerrado')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')

	class Meta:
		ordering=["numero"]
		verbose_name='Pedidos Caja'
		verbose_name_plural='Pedidos Caja'

	def __str__(self):
		return self.numero		
		

class PedidoCajaDetalle(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCaja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='pedido_caja_detalle_tipodocumento')
	IdPedidoCaja = models.ForeignKey(PedidoCaja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='pedido_caja_detalle_pedido')
	IdItem = models.ForeignKey(MaestroItem,max_length=20,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item Inventario',related_name='pedido_caja_detalle_item')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	cantidad = models.IntegerField(default=0,verbose_name='Cantidad')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Total')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Detalle Pedidos Caja'
		verbose_name_plural='Detalle Pedidos Caja'

	def __str__(self):
		return self.IdTipoDocumento.descripcion+'-'+self.numero

class SesionCaja(models.Model):
	IdCaja = models.ForeignKey(Caja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Caja',related_name='sesion_caja_caja')
	IdSucursal = models.ForeignKey(Sucursal,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name="sesion_caja_sucursal")	# SUCURSAL
	IdUsuario = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Usuario',related_name="sesion_caja_usuario") # USUARIO
	abierta = models.BooleanField(default=False,verbose_name='Abierta')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')

	class Meta:
		ordering=["IdCaja"]
		verbose_name='Sesión Caja'
		verbose_name_plural='Sesiones Caja'

	def __str__(self):
		return self.IdCaja	


class TipoPagoReciboCaja(models.Model):
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción',unique=True)
	
	class Meta:
		ordering=["descripcion"]
		verbose_name='Tipo Pago'
		verbose_name_plural='Tipos Pago'

	def __str__(self):
		return self.descripcion

class TarjetaCredito(models.Model):
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción',unique=True)
	
	class Meta:
		ordering=["descripcion"]
		verbose_name='Tarjeta Crédito'
		verbose_name_plural='Tarjetas de Crédito'

	def __str__(self):
		return self.descripcion

class ReciboCaja(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCaja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='recibo_caja_tipodocumento')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	pagado = models.BooleanField(default=False,verbose_name='Pagado')
	pedido_caja = models.CharField(max_length=20,null=False,blank=False,verbose_name='Pedido Caja')
	registro = models.CharField(max_length=20,null=False,blank=False,verbose_name='No. Registro')
	IdTercero = models.ForeignKey(Tercero,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Cliente:',related_name='recibo_caja_tercero')
	IdMesa = models.ForeignKey(Mesa,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Mesa',related_name='recibo_caja_mesa')
	IdHabitacion = models.ForeignKey(Habitacion,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Habitacion',related_name='recibo_caja_habitacion')
	IdCaja = models.ForeignKey(Caja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Caja No.',related_name='recibo_caja_caja')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='recibo_caja_sucursal')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='recibo_caja_centro_costo')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Recibo Caja'
		verbose_name_plural='Recibos Caja'

	def __str__(self):
		return self.numero		

class ReciboCajaDetalle(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCaja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo documento',related_name='recibo_caja_detalle_tipo_documento')
	IdReciboCaja = models.ForeignKey(ReciboCaja,max_length=10,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Recibo Caja',related_name='recibo_caja_detalle_recibo_caja')
	IdPedidoCajaDetalle = models.ForeignKey(PedidoCajaDetalle,max_length=10,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Pedido Caja',related_name='recibo_caja_detalle_pedido_caja')
	pedido_caja = models.CharField(max_length=20,null=False,blank=False,verbose_name='Pedido Caja')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdItem = models.ForeignKey(MaestroItem,max_length=20,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item Inventario',related_name='recibo_caja_detalle_item')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	cantidad = models.IntegerField(default=0,verbose_name='Cantidad')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Total')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Detalle Recibo Caja'
		verbose_name_plural='Detalle Recibos Caja'

	def __str__(self):
		return self.IdTipoDocumento.descripcion+'-'+self.numero		
		
class PagoReciboCaja(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCaja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo documento',related_name='pago_caja_detalle_tipo_documento')
	IdTipoPago = models.ForeignKey(TipoPagoReciboCaja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Pago',related_name='pago_caja_tipopago')
	IdCaja = models.ForeignKey(Caja,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Caja Pago',related_name='pago_caja_caja')
	IdTercero = models.ForeignKey(Tercero,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Cliente:',related_name='pago_caja_tercero')
	recibo_caja = models.CharField(max_length=20,null=False,blank=False,verbose_name='Recibo Caja')
	IdTarjetaCredito = models.ForeignKey(TarjetaCredito,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tarjeta de Crédito',related_name='pago_caja_tarjeta_credito')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	estado = models.BooleanField(default=1,verbose_name='Estado')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='pago_caja_sucursal')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='pago_caja_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')		

	class Meta:
		ordering=["numero"]
		verbose_name='Pago Caja'
		verbose_name_plural='Pagos Caja'

	def __str__(self):
		return self.IdTipoDocumento.descripcion+'-'+self.numero		