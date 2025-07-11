from django.contrib import admin
from .models import TipoDocumentoCocina,OrdenProduccionIngrediente,Receta,Ingrediente,OrdenProduccion,RecetaIngrediente
from import_export import fields,resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class TipoDocumentoCocinaResource(resources.ModelResource):
    class Meta:
        model = TipoDocumentoCocina
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipo','descripcion','numeracion','caracteres','longitud','actual')        
        exclude = ('id',)

@ admin.register (TipoDocumentoCocina)

class TipoDocumentoCocina(ImportExportModelAdmin):
    list_display= ('idTipo','descripcion','numeracion','caracteres','longitud','actual')
    search_fields = ['idTipo','descripcion']
    list_per_page = 30

class RecetaResource(resources.ModelResource):
    class Meta:
        model = Receta
        skip_unchanged = True
        report_skipped = True
        fields = ('producto')        
        exclude = ('id',)

@ admin.register (Receta)

class Receta(ImportExportModelAdmin):
    list_display= ('producto',)
    search_fields = ['producto',]
    list_per_page = 30

class RecetaIngredienteResource(resources.ModelResource):
    class Meta:
        model = RecetaIngrediente
        skip_unchanged = True
        report_skipped = True
        fields = ('receta','ingrediente','cantidad_necesaria')        
        exclude = ('id',)

@ admin.register (RecetaIngrediente)

class RecetaIngrediente(ImportExportModelAdmin):
    list_display= ('receta','ingrediente','cantidad_necesaria')
    search_fields = ['receta','ingrediente','cantidad_necesaria']
    list_per_page = 30

class OrdenProduccionResource(resources.ModelResource):
    class Meta:
        model = OrdenProduccion
        skip_unchanged = True
        report_skipped = True
        fields = ('fecha','numero','receta','cantidad_producir','costo_orden','estado','IdUsuario','updated')        
        exclude = ('id',)

@ admin.register (OrdenProduccion)

class OrdenProduccion(ImportExportModelAdmin):
    list_display= ('fecha','numero','receta','cantidad_producir','costo_orden','estado','IdUsuario','updated')
    search_fields = ['fecha','numero','receta']
    list_per_page = 30

class OrdenProduccionIngredienteResource(resources.ModelResource):
    class Meta:
        model = OrdenProduccionIngrediente
        skip_unchanged = True
        report_skipped = True
        fields = ('orden','ingrediente','cantidad_necesaria','cantidad_stock','cantidad_a_comprar','precio_compra_unitario','costo_compra')        
        exclude = ('id',)

@ admin.register (OrdenProduccionIngrediente)

class OrdenProduccionIngrediente(ImportExportModelAdmin):
    list_display= ('orden','ingrediente','cantidad_necesaria','cantidad_stock','cantidad_a_comprar','precio_compra_unitario','costo_compra')
    search_fields = ['orden','ingrediente']
    list_per_page = 30