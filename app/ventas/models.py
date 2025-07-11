from django.db import models

# Create your models here.

from datetime import date
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum
from core.models import Tercero,Sucursal
from inventarios.models import MaestroItem 

class TipoDocumentoVenta(models.Model):
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

##Contado,Crédito
class FormaPago(models.Model):
	idFormaPago=models.CharField(max_length=2,unique=True,verbose_name='Código Forma de Pago')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	credito=models.BooleanField(default=False,verbose_name='Crédito')    

	class Meta:
		ordering=["descripcion"]
		verbose_name='Forma de Pago'
		verbose_name_plural='Formas de Pago'

	def __str__(self):
		return self.descripcion
	
class Cotizacion(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoVenta,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='cotizacion_tipodocumento')
	cliente = models.CharField(max_length=100,null=False,blank=False,verbose_name='Cliente')
	factura = models.CharField(max_length=10,default='',verbose_name='Factura')
	fecha = models.DateField(null=True,blank=True,default=None,verbose_name='Fecha')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='cotizacion_sucursal')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='cotizacion_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Cotizacion'
		verbose_name_plural='Cotizaciones'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero

class CotizacionDetalle(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoVenta,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='factura_detalle_tipodocumento')
	IdItem =  models.ForeignKey(MaestroItem,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item',related_name='cotizacion_detalle_item')
	cantidad = models.IntegerField(default=0,verbose_name='Cantidad')
	valor_unit = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Unitario')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Total')
	por_iva = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='% Iva')
	val_iva = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Iva')
	por_desc = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='% Descuento')
	val_desc = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Descuento')
	valor_neto = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Neto')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Detalle Factura'
		verbose_name_plural='Detalle Facturas'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero


FORMA_PAGO = (
		('CO','Contado'),
		('CR','Crédito'),
		)
class FacturaVenta(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoVenta,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='factura_venta_tipodocumento')
	IdTercero = models.ForeignKey(Tercero,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tercero',related_name='factura_venta_tercero')
	forma_pago = models.CharField(max_length=10,default='CO',choices=FORMA_PAGO,verbose_name='Forma De Pago')
	fecha = models.DateField(null=True,blank=True,default=None,verbose_name='Fecha')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='factura_venta_sucursal')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='factura_venta_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Factura Venta'
		verbose_name_plural='Facturas Venta'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero

class FacturaVentaDetalle(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoVenta,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='factura_venta_detalle_tipodocumento')
	IdFactura =  models.ForeignKey(FacturaVenta,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Factura',related_name='factura_venta_detalle_factura')
	IdItem =  models.ForeignKey(MaestroItem,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item',related_name='factura_venta_detalle_item')
	cantidad = models.IntegerField(default=0,verbose_name='Cantidad')
	valor_unit = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Unitario')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Total')
	por_iva = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='% Iva')
	val_iva = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Iva')
	por_desc = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='% Descuento')
	val_desc = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Descuento')
	valor_neto = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Neto')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Detalle Factura Venta'
		verbose_name_plural='Detalle Facturas Venta'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero
	
class NotaCredito(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoVenta,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='nota_credito_tipodocumento')
	IdFacturaVenta = models.ForeignKey(FacturaVenta,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Recibo Caja',related_name='nota_credito_factura_venta')
	IdTercero = models.ForeignKey(Tercero,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tercero',related_name='nota_credito_tercero')
	fecha = models.DateField(null=True,blank=True,default=None,verbose_name='Fecha')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='nota_credito_sucursal')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='nota_credito_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Nota Crédito'
		verbose_name_plural='Notas Crédito'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero

