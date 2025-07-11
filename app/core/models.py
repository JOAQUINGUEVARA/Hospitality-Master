from django.db import models

# Create your models here.

from datetime import date
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import Sum

class Empresa(models.Model):
	nombre = models.CharField(max_length=80,null=False,blank=False,verbose_name='Nombre Empresa')
	nit = models.CharField(max_length=15,null=False,blank=False,verbose_name='Nit Empresa')
	direccion = models.CharField(max_length=50,null=False,blank=False,verbose_name='Dirección Empresa')
	telefonos = models.CharField(max_length=50,null=False,blank=False,verbose_name='Teléfono Empresa')

	class Meta:
		ordering=["nombre"]
		verbose_name='Empresa'
		verbose_name_plural='Empresas'
		
	def __str__(self):
		return self.nit+'-'+self.nombre
	
class Pais(models.Model):
	idPais = models.CharField(max_length=3,null=False,blank=False,unique=True,default=1,verbose_name='Código País')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	
	class Meta:
		ordering=["descripcion"]
		verbose_name='Pais'
		verbose_name_plural='Paises'
		
	def __str__(self):
		return self.descripcion

class Departamento(models.Model):
	idDepartamento = models.CharField(max_length=3,null=False,blank=False,default=1,verbose_name='Código Departamento')
	IdPais = models.ForeignKey(Pais,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Código País',related_name='departamento_pais')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	
	class Meta:
		ordering=["descripcion"]
		verbose_name='Departamento'
		verbose_name_plural='Departamentos'

	def __str__(self):
		return self.descripcion

class Ciudad(models.Model):
	idCiudad=models.CharField(max_length=5,null=False,blank=False,default=1,verbose_name='Código Ciudad')
	IdPais = models.ForeignKey(Pais,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='País',related_name='ciudad_pais')
	IdDepartamento = models.ForeignKey(Departamento,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Departamento',related_name='ciudad_departamento')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	
	class Meta:
		ordering=["descripcion"]
		verbose_name='Ciudad'
		verbose_name_plural='Ciudad'
		
	def __str__(self):
		return self.descripcion
	
class TipoIdentificacion(models.Model):
	idTipoIdentificacion = models.CharField(max_length=2,null=False,blank=False,unique=True,default=1,verbose_name='Código Identificación')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	class Meta:
		ordering=["descripcion"]
		verbose_name='Tipo de Identificación'
		verbose_name_plural='Tipos de Identificación'
	
	def __str__(self):
		return self.descripcion


class Tercero(models.Model):
	identificacion= models.CharField(max_length=15,null=True,blank=True,default='',unique=True,verbose_name='Nro. Identificación')
	IdTipoIdentificacion=models.ForeignKey(TipoIdentificacion,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo de Indetificación',related_name='tercero_tipoidentificacion')
	#IdTipoTercero=models.ForeignKey(TipoTercero,max_length=2,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='Tipo de Tercero',related_name='tercero_tipoidentificacion') #IdTipoIdentificacion
	identifica_de = models.CharField(default='',max_length=100,verbose_name='Identificacion de')
	nombre1 = models.CharField(max_length=25,blank=True,default='',verbose_name='Primer Nombre')
	nombre2 = models.CharField(max_length=25,blank=True,default='',verbose_name='Segundo Nombre')
	apel1 = models.CharField(max_length=25,blank=True,default='',verbose_name='Primer Apellido')
	apel2 = models.CharField(max_length=25,blank=True,default='',verbose_name='Segundo Apellido')
	apenom = models.CharField(max_length=80,default='',verbose_name='Nombre')
	ocupacion = models.CharField(max_length=80,default='',verbose_name='Ocupación')
	razon_social = models.CharField(max_length=70,null=True,blank=True,default='',verbose_name='Razon Social')
	nombre = models.CharField(max_length=70,null=True,blank=True,default='',verbose_name='Nombre')
	direccion = models.TextField(blank=True,default='',verbose_name='Dirección')
	telefono = models.TextField(blank=True,default='',verbose_name='Teléfono')
	email = models.EmailField(max_length=254,null=True,blank=True,default='',verbose_name='Email')
	IdPais = models.ForeignKey(Pais,null=False,blank=False,default=1,on_delete=models.CASCADE,verbose_name='País',related_name='tercero_pais')
	departamento = models.CharField(default='',max_length=100,verbose_name='Departamento')
	ciudad = models.CharField(default='',max_length=100,verbose_name='Ciudad')
	contacto = models.CharField(default='',max_length=100,verbose_name='Contacto')
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
		verbose_name='Tercero'
		verbose_name_plural='Terceros'

	def __str__(self):
		if self.razon_social==self.apenom:
			return self.identificacion.strip()+"-"+str(self.razon_social).strip()
		else:
			return self.identificacion.strip()+"-"+str(self.razon_social).strip()+"-"+str(self.apenom).strip()

class Sucursal(models.Model):
	idSucursal = models.CharField(max_length=3,null=False,blank=False,unique=True,verbose_name='Código Sucursal')
	descripcion=models.TextField(blank=True,default='',verbose_name='Sucursal')

	class Meta:
		ordering=["descripcion"]
		verbose_name='Sucursal'
		verbose_name_plural='Sucursales'

	def __str__(self):
		return self.descripcion
	
class ValorDefecto(models.Model):
	idValor = models.CharField(max_length=2,null=False,blank=False,unique=True,verbose_name='Código Valor')
	valor = models.CharField(max_length=10,null=False,blank=False,default=1,verbose_name='Valor')
	descripcion=models.TextField(blank=True,default='',verbose_name='Descripción')
	class Meta:
		ordering=["descripcion"]
		verbose_name='Valor Defecto'
		verbose_name_plural='Valores Defecto'
	
	def __str__(self):
		return self.descripcion
	
class Anio(models.Model):
	anio=models.CharField(max_length=4,default='',verbose_name='Año',unique=True,)
	
	class Meta:
		ordering=["anio"]
		verbose_name='Año'
		verbose_name_plural='Años'
		
	def __str__(self):
		return self.anio
	
class Mes(models.Model):
	idMes=models.CharField(max_length=2,default='',verbose_name='Mes',unique=True,)
	descripcion=models.CharField(max_length=15,default='',verbose_name='Mes')
	
	class Meta:
		ordering=["idMes"]
		verbose_name='Mes'
		verbose_name_plural='Meses'
		
	def __str__(self):
		return self.descripcion	
	
