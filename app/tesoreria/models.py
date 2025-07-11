from django.db import models
from datetime import date
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum

from core.models import Tercero,Sucursal
from ventas.models import FacturaVenta
#from caja.models import ReciboCaja
from cxc.models import Cartera
from cxp.models import FacturaCompra


class TipoDocumentoTes(models.Model):
	idTipo = models.CharField(max_length=3,blank=True,unique=True,verbose_name='Código Tipo Documento')
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

class Banco(models.Model):
	idBanco=models.CharField(max_length=3,blank=True,unique=True,verbose_name='Código Banco')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	sucursal=models.CharField(max_length=100,blank=True,default='',verbose_name='Sucursal')
	cuenta_no=models.CharField(max_length=15,blank=True,default='',verbose_name='Número de Cuenta')
	telefonos=models.CharField(max_length=60,blank=True,default='',verbose_name='Teléfonos')
	responsable=models.CharField(max_length=60,blank=True,default='',verbose_name='Responsable')
	email_respons=models.EmailField(max_length=254,blank=True,default='',verbose_name='Email Eesponsable')
	debitos = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Débitos' )
	creditos = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Créditos' )
	saldo = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Saldo' )
		
	class Meta:
		ordering=["descripcion"]
		verbose_name='Banco'
		verbose_name_plural='Bancos'

	def __str__(self):
		return self.descripcion
	
	
class PagoProveedor(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoTes,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='pago_proveedor_tipodocumento')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	IdFacturaCompra = models.ForeignKey(FacturaCompra,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Factura',related_name='pago_proveedor_factura')
	IdTercero = models.ForeignKey(Tercero,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Cliente',related_name='pago_proveedor_cliente')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='pago_proveedor_sucursal')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='pago_proveedor_usuario')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Pago Proveedor'
		verbose_name_plural='Pago Proveedores'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero

class IngresoPagoCartera(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoTes,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='ingreso_pago_cartera_tipodocumento')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	IdCartera = models.ForeignKey(Cartera,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Factura',related_name='ingreso_pago_cartera_actura')
	IdTercero = models.ForeignKey(Tercero,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Cliente',related_name='ingreso_pago_cartera_cliente')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='ingreso_pago_cartera_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Ingreso Pago Cartera'
		verbose_name_plural='Ingresos Pago Cartera'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero
		
class Consignacion(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoTes,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='consignacion_tipodocumento')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdBanco = models.ForeignKey(Banco,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Banco',related_name='consignacion_banco')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='consignacion_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Consignacion'
		verbose_name_plural='Consignaciones'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero

