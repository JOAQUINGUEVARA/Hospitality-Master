from django.contrib import admin
from import_export import fields,resources
from import_export.admin import ImportExportModelAdmin
from cxc.models import TipoDocumentoCxC,Cartera
# Register your models here.

class TipoDocumentoCxCResource(resources.ModelResource):
    class Meta:
        model = TipoDocumentoCxC
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipo','descripcion','numeracion','caracteres','longitud','actual')        
        exclude = ('id',)

@ admin.register (TipoDocumentoCxC)
class TipoDocumentoCxC(ImportExportModelAdmin):
    list_display= ('idTipo','descripcion','numeracion','caracteres','longitud','actual')
    search_fields = ['descripcion']
    list_per_page = 30

class CarteraResource(resources.ModelResource):
    class Meta:
        model = Cartera
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','fecha','detalle','estado','IdTercero','IdSucursal','IdUsuario','valor','created','updated')        
        exclude = ('id',)

@ admin.register (Cartera)
class Cartera(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','fecha','detalle','estado','IdTercero','IdSucursal','IdUsuario','valor','created','updated')
    search_fields = ['descripcion']
    list_per_page = 30

