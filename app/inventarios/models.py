# Create your models here.
from django.db import models
from datetime import date
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum

from core.models import Sucursal,Tercero,Anio,Mes
from compras.models import OrdenCompra,DetalleDespacho,Proveedor

from django.core.exceptions import ValidationError


#from ventas.models import FacturaVenta
#from caja.models import ReciboCaja

# Create your models here.

#CURRENCY = settings.CURRENCY

class Bodega(models.Model):
	idBodega=models.CharField(max_length=3,blank=True,default='',unique=True,verbose_name='Código Bodega')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripcion')
	direccion=models.CharField(max_length=200,blank=True,default='',verbose_name='Dirección')
	telefonos=models.CharField(max_length=100,blank=True,default='',verbose_name='Teléfonos')
	responsable=models.CharField(max_length=100,blank=True,default='',verbose_name='Responsable')
	email_bodega=models.EmailField(max_length=254,blank=True,default='',verbose_name='Email Bodega')
	IdSucursal = models.ForeignKey(Sucursal,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='bodega_sucursal')
	class Meta:
		ordering=["descripcion"]
		verbose_name='Bodega'
		verbose_name_plural='Bodegas'
	def __str__(self):
		return self.descripcion
	
class TipoDocumentoInv(models.Model):
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
	
class Grupo(models.Model):
	#idGrupo=models.CharField(max_length=2,blank=True,default='',unique=True,verbose_name='Código Grupo')
	descripcion=models.TextField(blank=True,default='',unique=True,verbose_name='Descripción')
	IdBodega = models.ForeignKey(Bodega,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Bodega',related_name='grupo_bodega')
	
	class Meta:
		ordering=["descripcion"]
		verbose_name='Grupo'
		verbose_name_plural='Grupos'
	def __str__(self):
		return self.descripcion

class SubGrupo(models.Model):
	#idSubGrupo=models.CharField(max_length=3,blank=True,default='',unique=True,verbose_name='Código SubGrupo')
	IdGrupo=models.ForeignKey(Grupo,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Grupo',related_name='subgrupo_grupo')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	
	class Meta:
		ordering=["descripcion"]
		verbose_name='SubGrupo'
		verbose_name_plural='SubGrupos'
	def __str__(self):
		return self.descripcion

""" class UnidadMedida(models.Model):
	idMedida=models.CharField(max_length=2,blank=True,default='',unique=True,verbose_name='Código Medida')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	
	class Meta:
		ordering=["descripcion"]
		verbose_name='Medida'
		verbose_name_plural='Medidas'
	def __str__(self):
		return self.descripcion """

class Medida(models.Model):
	idMedida = models.CharField(max_length=2, unique=True, verbose_name="Id. Unidad")
	descripcion = models.CharField(max_length=50, unique=True, verbose_name="Nombre Unidad") # Ej: Kilogramo, Litro, Unidad
	#abreviatura = models.CharField(max_length=10, unique=False, verbose_name="Abreviatura") # Ej: kg, L, und
	
	def __str__(self):
		return f"{self.descripcion}"
	# ({self.abreviatura})
	class Meta:
		verbose_name = "Unidad de Medida"
		verbose_name_plural = "Unidades de Medida"

""" class Ingrediente(models.Model):
	IdMaestroItem = models.ForeignKey('MaestroItem', on_delete=models.PROTECT,verbose_name='Ingrediente')
	nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Ingrediente")
	descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
	unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, verbose_name="Unidad de Medida")
	cantidad_stock = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, verbose_name="Cantidad en Stock")
	stock_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, verbose_name="Stock Mínimo (Opcional)")
	# precio_compra_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio de Compra Unitario")

	def __str__(self):
		return f"{self.nombre} ({self.cantidad_stock} {self.unidad_medida.abreviatura})"
	
	def aumentar_stock(self, cantidad):
		self.cantidad_stock += cantidad
		self.save()
	
	def disminuir_stock(self, cantidad):
		if self.cantidad_stock >= cantidad:
			self.cantidad_stock -= cantidad
			self.save()
		else:
			raise ValidationError(f"No hay suficiente stock de {self.nombre}. Stock actual: {self.cantidad_stock} {self.unidad_medida.abreviatura}, se intentó reducir: {cantidad} {self.unidad_medida.abreviatura}") """


class MaestroItem(models.Model):
	TIPO_ITEM = (
		('PT','Producto Terminado'),
		('MP','Materia Prima'),
		('SP','Servicio'),
		('AV','Articulo Venta'),		
		)
	#idItem=models.CharField(max_length=20,default='',verbose_name='Código Item')
	IdGrupo=models.ForeignKey(Grupo,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Grupo',related_name='item_grupo')
	IdSubGrupo=models.ForeignKey(SubGrupo,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Subgrupo',related_name='item_subgrupo')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	IdUnidadMedida=models.ForeignKey(Medida,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Unidad de Medida',related_name='item_unidad_medida')
	marca=models.CharField(max_length=100,blank=True,default='',verbose_name='marca')
	referencia_fabrica=models.CharField(max_length=100,blank=True,default='',verbose_name='referencia_fabrica')
	valor_venta = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Venta')
	valor_compra = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Compra')
	tipo_producto = models.CharField(max_length=2,blank=True,default='PT',choices=TIPO_ITEM,verbose_name='Tipo Producto')
	por_iva = models.IntegerField(default=0,verbose_name='% Iva')
	cant_maxima = models.IntegerField(default=0,verbose_name='Cantidad Máxima')
	cant_minima = models.IntegerField(default=0,verbose_name='Cantidad Mínima')
	costo_prom = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Costo Promedio')
	IdBodega = models.ForeignKey(Bodega,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Bodega',related_name='item_bodega')
	imagen = models.ImageField(upload_to='media/',default='core/static/img/placefolder.png')
	acumula = models.BooleanField(default='True',verbose_name='Acumula')
	estadia = models.BooleanField(default='False',verbose_name='Estadia')
	""" ingredientes_requeridos = models.ManyToManyField(
        Ingrediente,
        through='IngredienteProducto',
        related_name='productos_compuestos',
        verbose_name="Ingredientes Requeridos"
    ) """
	class Meta:
		ordering=["descripcion"]
		verbose_name='Maestro de Item'
		verbose_name_plural='Maestro de Items'
		
	def __str__(self):
		return f"{self.descripcion} "
	
	""" def aumentar_stock(self, cantidad):
		self.cantidad_stock += cantidad 
		self.save() """
		
	""" def disminuir_stock(self, cantidad):
		if self.cantidad_stock >= cantidad:
			self.cantidad_stock -= cantidad
			self.save()
		else:
			raise ValidationError(f"No hay suficiente stock de {self.nombre}. Stock actual: {self.cantidad_stock} {self.unidad_medida.abreviatura}, se intentó reducir: {cantidad} {self.unidad_medida.abreviatura}") """

	#def descontar_ingredientes_de_stock(self, cantidad_productos_salientes):
		#ingredientes_producto = IngredienteProducto.objects.filter(producto=self)
		#for item_receta in ingredientes_producto:
			#cantidad_a_descontar = item_receta.cantidad_necesaria * cantidad_productos_salientes
			#try:
			#	item_receta.ingrediente.disminuir_stock(cantidad_a_descontar)
            #    # Opcional: Registrar este movimiento específico de ingrediente
			#	MovimientoInventario.objects.create(
            #    tipo_movimiento=MovimientoInventario.AJUSTE_PRODUCCION_SALIDA_INGREDIENTE,
            #    ingrediente_afectado=item_receta.ingrediente,
            #    cantidad=cantidad_a_descontar,
            #    descripcion=f"Descuento por salida de {cantidad_productos_salientes} unds del producto {self.nombre}"
            #    )
            #except ValidationError as e:
            # Manejar el error, por ejemplo, registrarlo o revertir la salida del producto si es crítico
			#print(f"Error al descontar ingrediente {item_receta.ingrediente.nombre}: {e}")
            # Aquí podrías lanzar una excepción más arriba para revertir la transacción de salida del producto.
            #raise ValidationError(f"Insuficiente stock del ingrediente '{item_receta.ingrediente.nombre}' para producir {cantidad_productos_salientes} de '{self.nombre}'. Error: {e}")

	class Meta:
		verbose_name = "Producto Terminado"
		verbose_name_plural = "Productos Terminados"


class IngredienteProducto(models.Model): # Modelo intermedio para la formulación (Receta)
    producto = models.ForeignKey(MaestroItem, on_delete=models.CASCADE, verbose_name="Producto")
    #ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, verbose_name="Ingrediente")
    cantidad_necesaria = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Cantidad Necesaria del Ingrediente")
    # La unidad de medida de la cantidad necesaria es la del Ingrediente referenciado.

    def __str__(self):
        return f"{self.cantidad_necesaria} {self.producto.IdUnidadMedida.abreviatura} de {self.producto.descripcion} para {self.producto.descripcion}"

    class Meta:
        #unique_together = ('producto', 'ingrediente') # Un ingrediente solo puede estar una vez por producto
        verbose_name = "Ingrediente por Producto (Receta)"
        verbose_name_plural = "Ingredientes por Producto (Recetas)"

class AcumuladoItem(models.Model):
	IdItem=models.ForeignKey(MaestroItem,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Acumulado Items',related_name='acumulado_item')
	IdSucursal = models.ForeignKey(Sucursal,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Acumulado Sucursal',related_name='acumulado_item_sucursal')
	IdBodega = models.ForeignKey(Bodega,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Acumulado Bodega',related_name='acumulado_Item_bodega')
	cant_maxima = models.IntegerField(default=0,verbose_name='Cantidad Máxima')
	cant_minima = models.IntegerField(default=0,verbose_name='Cantidad Mínima')
	costo_prom = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Costo Promedio')
	anio=models.CharField(max_length=4,default='',verbose_name='Año')

	ii_01 = models.IntegerField(default=0,verbose_name='Inv. Inic. Enero')
	ent_01 = models.IntegerField(default=0,verbose_name='Entradas Enero')
	sal_01 = models.IntegerField(default=0,verbose_name='Salidas Enero')
	if_01 = models.IntegerField(default=0,verbose_name='Inv. Final Enero')
	
	ii_02 = models.IntegerField(default=0,verbose_name='Inv. Inic. Febrero')
	ent_02 = models.IntegerField(default=0,verbose_name='Entradas Febrero')
	sal_02 = models.IntegerField(default=0,verbose_name='Salidas Febrero')
	if_02= models.IntegerField(default=0,verbose_name='Inv. Final Febrero')

	ii_03 = models.IntegerField(default=0,verbose_name='Inv. Inic. Marzo')
	ent_03 = models.IntegerField(default=0,verbose_name='Entradas Marzo')
	sal_03 = models.IntegerField(default=0,verbose_name='Salidas Marzo')
	if_03= models.IntegerField(default=0,verbose_name='Inv. Final Marzo')

	ii_04 = models.IntegerField(default=0,verbose_name='Inv. Inic. Abril')
	ent_04 = models.IntegerField(default=0,verbose_name='Entradas Abril')
	sal_04 = models.IntegerField(default=0,verbose_name='Salidas Abril')
	if_04= models.IntegerField(default=0,verbose_name='Inv. Final Abril')

	ii_05 = models.IntegerField(default=0,verbose_name='Inv. Inic. Mayo')
	ent_05 = models.IntegerField(default=0,verbose_name='Entradas Mayo')
	sal_05 = models.IntegerField(default=0,verbose_name='Salidas Mayo')
	if_05= models.IntegerField(default=0,verbose_name='Inv. Final Mayo')

	ii_06 = models.IntegerField(default=0,verbose_name='Inv. Inic. Junio')
	ent_06 = models.IntegerField(default=0,verbose_name='Entradas Junio')
	sal_06 = models.IntegerField(default=0,verbose_name='Salidas Junio')
	if_06= models.IntegerField(default=0,verbose_name='Inv. Final Junio')

	ii_07 = models.IntegerField(default=0,verbose_name='Inv. Inic. Julio')
	ent_07 = models.IntegerField(default=0,verbose_name='Entradas Julio')
	sal_07 = models.IntegerField(default=0,verbose_name='Salidas Julio')
	if_07= models.IntegerField(default=0,verbose_name='Inv. Final Julio')

	ii_08 = models.IntegerField(default=0,verbose_name='Inv. Inic. Agosto')
	ent_08 = models.IntegerField(default=0,verbose_name='Entradas Agosto')
	sal_08 = models.IntegerField(default=0,verbose_name='Salidas Agosto')
	if_08= models.IntegerField(default=0,verbose_name='Inv. Final Agosto')

	ii_09 = models.IntegerField(default=0,verbose_name='Inv. Inic. Sept.')
	ent_09 = models.IntegerField(default=0,verbose_name='Entradas Sept.')
	sal_09 = models.IntegerField(default=0,verbose_name='Salidas Sept.')
	if_09= models.IntegerField(default=0,verbose_name='Inv. Final Sept.')

	ii_10 = models.IntegerField(default=0,verbose_name='Inv. Inic. Oct.')
	ent_10 = models.IntegerField(default=0,verbose_name='Entradas Oct.')
	sal_10 = models.IntegerField(default=0,verbose_name='Salidas Oct.')
	if_10= models.IntegerField(default=0,verbose_name='Inv. Final Oct.')
	
	ii_11 = models.IntegerField(default=0,verbose_name='Inv. Inic. Nov.')
	ent_11 = models.IntegerField(default=0,verbose_name='Entradas Nov.')
	sal_11 = models.IntegerField(default=0,verbose_name='Salidas Nov.')
	if_11= models.IntegerField(default=0,verbose_name='Inv. Final Nov.')

	ii_12 = models.IntegerField(default=0,verbose_name='Inv. Inic. Dic.')
	ent_12 = models.IntegerField(default=0,verbose_name='Entradas Dic.')
	sal_12 = models.IntegerField(default=0,verbose_name='Salidas Dic.')
	if_12= models.IntegerField(default=0,verbose_name='Inv. Final Dic.')

	class Meta:
		ordering=["IdItem"]
		verbose_name='Acumulado Inventario'
		verbose_name_plural='Acumulados Inventario'
	
	def __str__(self):
		return self.IdItem.descripcion

class InventarioFisico(models.Model):

	IdItem=models.ForeignKey(MaestroItem,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Acumulado Items',related_name='invntario_fisico_item')
	IdSucursal = models.ForeignKey(Sucursal,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Acumulado Sucursal',related_name='inventario_fisico_sucursal')
	IdBodega = models.ForeignKey(Bodega,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Acumulado Bodega',related_name='inventario_fisico_bodega')
	IdAnio=models.ForeignKey(Anio,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Año',related_name='inventario_fisico_anio')
	IdMes=models.ForeignKey(Mes,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Mes',related_name='inventario_fisico_mes')
	inv_fis = models.IntegerField(default=0,verbose_name='Inv. Fisico')
	inv_acum = models.IntegerField(default=0,verbose_name='Stock')
	diferencia = models.IntegerField(default=0,verbose_name='Diferencia')
	cerrado = models.BooleanField(default=False,verbose_name='Cerrado')
	numero_ajuste=models.CharField(max_length=20,verbose_name='Documento Ajuste')
	
	class Meta:
		ordering=["IdItem"]
		verbose_name='Inventario Físico'
		verbose_name_plural='Inventario Físico'
	
	def __str__(self):
		return self.IdItem.descripcion

class CierreInventario(models.Model):
	anio=models.CharField(max_length=4,default='',verbose_name='Año')
	cerrado = models.BooleanField(default=False,verbose_name='Cerrado')

	class Meta:
		ordering=["anio"]
		verbose_name='Cierre Inventario'
		verbose_name_plural='Cierre Inventario'
	
	def __str__(self):
		return self.anio
	

class Entrada(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoInv,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='entrada_tipodocumento')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	anio = models.CharField(max_length=4,null=False,blank=False,default='',verbose_name='Año')
	IdProveedor=models.ForeignKey(Proveedor,max_length=15,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Proveedor',related_name='entrada_proveedor')
	factura_compra=models.CharField(max_length=15,default='',verbose_name='Factura')
	orden_compra=models.CharField(max_length=15,default='',verbose_name='Orden de Compra')
	despacho=models.CharField(max_length=15,default='',verbose_name='Despacho')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='entrada_sucursal')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='entrada_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Entrada'
		verbose_name_plural='Entradas'

	def __str__(self):
		return self.numero	
	

class EntradaDetalle(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoInv,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='entrada_detalle_tipodocumento')
	IdEntrada = models.ForeignKey(Entrada,max_length=10,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Entrada Inventario',related_name='entrada_detalle_entrada')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	IdItem = models.ForeignKey(MaestroItem,max_length=20,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item Inventario',related_name='entrada_detalle_item')
	IdBodega = models.ForeignKey(Bodega,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Bodega',related_name='entrada_detalle_bodega')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	cantidad = models.IntegerField(default=0,verbose_name='Cantidad')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Total')
	despacho_detalle_id = models.IntegerField(default=0,verbose_name='Detalle Despacho Id')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Detalle Entrada'
		verbose_name_plural='Detalle Entradas'

	def __str__(self):
		return self.numero	
	
class Salida(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoInv,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='salida_tipodocumento')
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	anio = models.CharField(max_length=4,null=False,blank=False,default='',verbose_name='Anio')
	pedido_caja=models.CharField(max_length=15,default='',verbose_name='Pedido Caja')
	detalle=models.TextField(blank=True,default='',verbose_name='Detalle')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='salida_sucursal')
	IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='salida_usuario')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Salida'
		verbose_name_plural='Salidas'

	def __str__(self):
		return self.numero	
	

class SalidaDetalle(models.Model):
	numero = models.CharField(max_length=10,null=False,blank=False,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoInv,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='salida_detalle_tipo_documento')
	IdSalida = models.ForeignKey(Salida,max_length=10,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Entrada Inventario',related_name='salida_detalle_tipo_entrada')
	estado = models.BooleanField(default=False,verbose_name='Estado')
	IdItem = models.ForeignKey(MaestroItem,max_length=20,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item Inventario',related_name='salida_detalle_item')
	IdBodega = models.ForeignKey(Bodega,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Bodega',related_name='salida_detalle_bodega')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	cantidad = models.IntegerField(default=0,verbose_name='Cantidad')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Total')
	pedido_detalle_id = models.IntegerField(default=0,verbose_name='Detalle Pedido Id')
	created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha de Creación')
	updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')
	
	class Meta:
		ordering=["numero"]
		verbose_name='Detalle Salida'
		verbose_name_plural='Detalle Salida'

	def __str__(self):
		return self.numero	
	
class ProveedorItem(models.Model):
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')
	IdTercero = models.ForeignKey(Tercero,max_length=15,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tercero',related_name='proveeedor_item_tercero')
	IdItem=models.ForeignKey(MaestroItem,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item Inventario',related_name='proveedor_item_item')
	#IdFacturaCompra=models.ForeignKey(FacturaCompra,max_length=15,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Factura',related_name='proveedor_item_factura')
	IdOrdenCompra=models.ForeignKey(OrdenCompra,max_length=10,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Orden de Compra',related_name='proveedor_item_orden_compra')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	cantidad = models.IntegerField(default=0,verbose_name='Cantidad')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Total')


	class Meta:
		ordering=["IdTercero"]
		verbose_name='Proveedor Item'
		verbose_name_plural='Proveedores Items'

	def __str__(self):
		return self.IdTipoDocumento+'-'+self.numero	

class Kardex(models.Model):
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')								 
	numero = models.CharField(max_length=10,null=False,blank=False,verbose_name='Número')
	IdTipoDocumento = models.ForeignKey(TipoDocumentoInv,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo Documento',related_name='kardex_detalle_tipodocumento')
	pedido_caja=models.CharField(max_length=15,default='',verbose_name='Pedido Caja')
	factura_compra=models.CharField(max_length=15,default='',verbose_name='Factura')
	orden_compra=models.CharField(max_length=15,default='',verbose_name='Orden de Compra')
	despacho=models.CharField(max_length=15,default='',verbose_name='Despacho')
	IdItem = models.ForeignKey(MaestroItem,max_length=20,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Item Inventario',related_name='kardex_detalle_item')
	valor = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor')
	cantidad = models.IntegerField(default=0,verbose_name='Cantidad')
	valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0,verbose_name='Valor Total')								 
	saldo = models.IntegerField(default=0,verbose_name='Saldo')
	tipo_mov = models.CharField(max_length=10,default='',verbose_name='Tipo Movimiento')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='kardex_sucursal')
	IdBodega = models.ForeignKey(Bodega,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Bodega',related_name='kardex_bodega')
	class Meta:
		ordering=["numero"]
		verbose_name='Kardex'
		verbose_name_plural='Kardex'

	def __str__(self):
		return self.IdItem.descripcion	

class AjusteInventarioFisico(models.Model):
	fecha = models.DateField(null=True,blank=True,verbose_name='Fecha')	
	IdAnio=models.ForeignKey(Anio,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Año',related_name='ajuste_inventario_fisico_anio')
	IdMes=models.ForeignKey(Mes,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Mes',related_name='ajuste_inventario_fisico_mes')
	IdSucursal = models.ForeignKey(Sucursal,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Sucursal',related_name='ajuste_sucursal')
	IdBodega = models.ForeignKey(Bodega,max_length=3,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Bodega',related_name='ajuste_bodega')
	numero_ajuste_entrada=models.CharField(max_length=20,default='',verbose_name='Documento Ajuste Entrada')
	numero_ajuste_salida=models.CharField(max_length=20,default='',verbose_name='Documento Ajuste Salida')								 
	class Meta:
		ordering=["IdAnio"]
		verbose_name='Ajuste'
		verbose_name_plural='Ajustes'

	def __str__(self):
		return self.numero_ajuste_entrada



