from django.db import models
from datetime import date
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum
# Create your models here.

from core.models import Sucursal,TipoIdentificacion,Pais,Ciudad,Departamento
#from inventarios.models import MaestroItem,Bodega
 
class TipoDocumentoCompra(models.Model):
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

class Proveedor(models.Model):

	identificacion= models.CharField(max_length=15,null=True,blank=True,default='',unique=True,verbose_name='Nro. Identificación') #NumeroIdentificacion
	IdTipoIdentificacion=models.ForeignKey(TipoIdentificacion,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo de Indetificación',related_name='proveedor_tipoidentificacion')
	nombre1 = models.CharField(max_length=25,blank=True,default='',verbose_name='Primer Nombre') #PrimerNombre
	nombre2 = models.CharField(max_length=25,blank=True,default='',verbose_name='Segundo Nombre') #SegundoNombre
	apel1 = models.CharField(max_length=25,blank=True,default='',verbose_name='Primer Apellido') #PrimerApellido
	apel2 = models.CharField(max_length=25,blank=True,default='',verbose_name='Segundo Apellido') #SegudoApellido
	apenom = models.CharField(max_length=80,default='',verbose_name='Nombre')
	razon_social = models.CharField(max_length=70,null=True,blank=True,default='',verbose_name='Razon Social') #RazonSocial
	#nombre = models.CharField(max_length=70,null=True,blank=True,default='',verbose_name='Nombre') #nombre
	direccion = models.TextField(blank=True,default='',verbose_name='Dirección') #Direccion
	telefono = models.TextField(blank=True,default='',verbose_name='Teléfono') #Telefonos
	email = models.EmailField(max_length=254,null=True,blank=True,default='',verbose_name='Email') #Email
	IdPais = models.ForeignKey(Pais,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='País',related_name='proveedor_pais') # IdPais
	departamento = models.CharField(blank=True,default='',max_length=50,verbose_name='Departamento') #IdDepartamento
	ciudad = models.CharField(blank=True,default='',max_length=50,verbose_name='Ciudad')
	contacto = models.CharField(blank=True,default='',max_length=100,verbose_name='Contacto') #Contacto
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario')
	por_ica = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name='% Ica')
	por_ret_fte = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name='% Ret Fte')
	valor_debitos = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name='Valor Debitos')
	valor_creditos = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name='Valor Créditos')
	valor_saldo = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name='Valor Saldo')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')

	
	class Meta:
		ordering=['identificacion']
		verbose_name='Proveedor'
		verbose_name_plural='Proveedores'

	def __str__(self):
		return str(self.razon_social)+'-'+self.apenom.strip()
	
class OrdenCompra(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCompra,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='orden_compra_tipodocumento')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	IdProveedor=models.ForeignKey(Proveedor,max_length=15,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Proveedor',related_name='orden_compra_proveedor')
	despacho = models.CharField(blank=True,default='',max_length=20,verbose_name='Despacho')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='orden_compra_sucursal')
	#IdBodega = models.ForeignKey('inventarios.Bodega',max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Bodega',related_name='orden_compra_bodega')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='orden_compra_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Orden Compra'
		verbose_name_plural='Ordenes Compra'

	def __str__(self):
		return self.numero	
	
class OrdenCompraDetalle(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCompra,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='orden_compra_detalle_tipodocumento') 
	estado = models.BooleanField(default=False,verbose_name='Estado')
	IdOrden = models.ForeignKey('OrdenCompra',max_length=20,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Orden Compra',related_name='orden_compra_orden_compra')	
	IdItem = models.ForeignKey('inventarios.MaestroItem',max_length=20,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item Inventario',related_name='orden_compra_detalle_item')
	valor_unidad_empaque = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Cada Empaque')
	valor_compra = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Compra')
	cantidad_unidad_empaque = models.IntegerField(default=0,verbose_name='Cantidad Unidades Empacado')
	cantidad_empaque = models.IntegerField(default=0,verbose_name='Cantidad Empaques Comprados')
	cantidad_unidades_compra = models.IntegerField(default=0,verbose_name='Cantidad Unidades Compradas')
	valor_unitario = models.DecimalField(default=0,max_digits=10, decimal_places=2,verbose_name='Valor Unitario')
	#valor_total = models.DecimalField(default=0,max_digits=10, decimal_places=2,verbose_name='Valor Total')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Detalle OrdenCompra'
		verbose_name_plural='Detalle OrdenCompra'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero	


class Despacho(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCompra,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='despacho_tipodocumento')
	IdOrdenCompra = models.ForeignKey(OrdenCompra,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Orden Compra',related_name='despacho_tipodocumento')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	IdProveedor = models.ForeignKey(Proveedor,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Proveedor',related_name='despacho_cliente')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='despacho_sucursal')
	#IdBodega = models.ForeignKey('inventarios.Bodega',max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Bodega',related_name='despacho_bodega')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='despacho_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Despacho'
		verbose_name_plural='Despacho'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero

class DetalleDespacho(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoCompra,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='despacho_detalle_tipo_documento')
	IdDespacho = models.ForeignKey(Despacho,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Despacho',related_name='despacho_detalle_despacho')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	IdItem = models.ForeignKey('inventarios.MaestroItem',max_length=20,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item Inventario',related_name='despacho_detalle_item')
	valor_unitario = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Unitario')
	cantidad_ordenada = models.IntegerField(default=0,verbose_name='Cantidad Ordenada')
	cantidad_enviada = models.IntegerField(default=0,verbose_name='Cantidad Enviada')
	cantidad_unidad_empaque = models.IntegerField(default=0,verbose_name='Cantidad Unidades Empacado')
	cantidad_unidades_enviadas = models.IntegerField(default=0,verbose_name='Cantidad Unidades Enviadas')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Total')
	#IdBodega = models.ForeignKey('inventarios.Bodega',max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Bodega',related_name='despacho_bodega')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Detalle Despacho'
		verbose_name_plural='Detalle Despachos'
		
	def __str__(self):
		return self.numero


class ProveedorItem(models.Model):
	IdProveedor=models.ForeignKey(Proveedor,max_length=15,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Proveedor',related_name='proveedor_item_proveedor')	
	IdItem = models.ForeignKey('inventarios.MaestroItem',max_length=20,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item Inventario',related_name='proveedor_item_detalle_item')
	
	class Meta:
		ordering=["IdItem"]
		verbose_name='Proveedor Item'
		verbose_name_plural='Proveedores Items'
		
	def __str__(self):
		return self.IdItem.descripcion

class EmpaqueItem(models.Model):
	IdItem = models.ForeignKey('inventarios.MaestroItem',max_length=20,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item Inventario',related_name='empaque_item')
	descripcion = models.TextField(blank=True, default='', verbose_name='Descripción')
	cantidad = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Cantidad')

	class Meta:
		ordering = ["descripcion"]
		verbose_name = 'Empaque'
		verbose_name_plural = 'Empaques'

	def __str__(self):
		return self.descripcion