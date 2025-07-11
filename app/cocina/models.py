from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest,HttpResponse, HttpRequest, JsonResponse,HttpResponseRedirect
from django.core import serializers
from django.core.serializers import serialize
from django.db.models import Q,Sum
from django.contrib.auth.models import User

from inventarios.models import MaestroItem,Medida

# Create your models here.

class TipoDocumentoCocina(models.Model):
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
     
class Ingrediente(models.Model):
    ingrediente = models.ForeignKey(MaestroItem, on_delete=models.CASCADE, verbose_name="Ingrediente")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    unidad_medida = models.ForeignKey(Medida, on_delete=models.PROTECT, verbose_name="Unidad de Medida")
    #cantidad_stock = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, verbose_name="Cantidad en Stock")
    #stock_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, verbose_name="Stock Mínimo (Opcional)")
    # precio_compra_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio de Compra Unitario")

    def __str__(self):
        #return f"{self.descripcion} ({self.cantidad_stock} {self.unidad_medida.descripcion})"
        return f"{self.descripcion}==>{self.unidad_medida.descripcion}"

    
class Receta(models.Model): # Modelo intermedio para la formulación (Receta)
    producto = models.ForeignKey(MaestroItem, on_delete=models.CASCADE, verbose_name="Producto")
    
    def __str__(self):
        return f"{self.producto.descripcion} ({self.producto.IdUnidadMedida.descripcion})"

    class Meta:
        #unique_together = ('producto', 'ingrediente') # Un ingrediente solo puede estar una vez por producto
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"

class RecetaIngrediente(models.Model): # Modelo intermedio para la formulación (Receta)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, verbose_name="Receta")
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, verbose_name="Ingrediente")
    cantidad_necesaria = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad Necesaria")
    # La unidad de medida de la cantidad necesaria es la del Ingrediente referenciado.

    def __str__(self):
        #return f"{self.cantidad_necesaria} {self.ingrediente.unidad_medida.descripcion} de {self.ingrediente.descripcion} para {self.receta.producto.descripcion}"
        return f"{self.ingrediente.descripcion} ({self.cantidad_necesaria} {self.ingrediente.unidad_medida.descripcion}) para {self.receta.producto.descripcion}"
    class Meta:
        #unique_together = ('producto', 'ingrediente') # Un ingrediente solo puede estar una vez por producto
        verbose_name = "Receta Ingrediente"
        verbose_name_plural = "Recetas Ingredientes"        


class OrdenProduccion(models.Model):
    numero = models.CharField(max_length=10,null=False,blank=False,unique=True,verbose_name='Número')
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, verbose_name="Receta")
    cantidad_producir = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad a Producir")
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('producido', 'Producido')], default='pendiente')
    IdUsuario = models.ForeignKey(User,max_length=5,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Usuario',related_name='orden_produccion_usuario')
    costo_orden = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Costo orden")
    updated=models.DateTimeField(auto_now=True,verbose_name='Fecha de Edición')

    def __str__(self):
        return f"Orden de {self.receta.producto.descripcion} ({self.cantidad_producir} {self.receta.producto.IdUnidadMedida.descripcion})"

class OrdenProduccionIngrediente(models.Model): # Modelo intermedio para la formulación (Receta)
    orden = models.ForeignKey(OrdenProduccion, on_delete=models.CASCADE, verbose_name="Orden de Produccion")
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, verbose_name="Ingrediente")
    cantidad_necesaria = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad Necesaria")
    cantidad_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Cantidad en Stock")
    cantidad_a_comprar = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Cantidad a Comprar")
    precio_compra_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prec.de Comp.Unit")
    costo_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Costo Compra")
    def __str__(self):
        #return f"{self.ingrediente.descripcion} ({self.cantidad_necesaria} {self.ingrediente.unidad_medida.descripcion})"
        return self.orden.numero
   
    class Meta:
        #unique_together = ('producto', 'ingrediente') # Un ingrediente solo puede estar una vez por producto
        verbose_name = "Orden Ingrediente"
        verbose_name_plural = "Ordenes Ingredientes"          