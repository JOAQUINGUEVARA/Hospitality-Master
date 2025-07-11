from django.db import models
from datetime import date
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum
# Create your models here.

from core.models import Tercero,Sucursal
from compras.models import OrdenCompra,Despacho
#from inventarios.models import MaestroItem 
 
class TipoDocumentoCxP(models.Model):
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
	
class FacturaCompra(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCxP,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='factura_compra_tippodocumento')
	IdOrdenCompra = models.ForeignKey(OrdenCompra,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Orden Compra',related_name='factura_compra_tipodocumento')
	IdDespacho = models.ForeignKey(Despacho,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Orden Compra',related_name='factura_compra_tipodocumento')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdTercero = models.ForeignKey(Tercero,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Cliente',related_name='factura_compra_cliente')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='factura_compra_sucursal')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='factura_compra_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Factura Compra'
		verbose_name_plural='Facturas Compra'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero
	
class FacturaCompraDetalle(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,verbose_name='Número')
	IdFacturaCompra = models.ForeignKey(FacturaCompra,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Factura Compra',related_name='factura_compra_detalle_despacho')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCxP,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='factura_compra_detalle_tipo_documento')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	IdItem = models.ForeignKey('inventarios.MaestroItem',max_length=20,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item Inventario',related_name='factura_compra_item')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	cantidad = models.IntegerField(default=0,verbose_name='Cantidad')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Total')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Detalle Factura Compra'
		verbose_name_plural='Detalle Facturas Compra'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero


