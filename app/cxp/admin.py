from django.contrib import admin
from import_export import fields,resources
from import_export.admin import ImportExportModelAdmin
from cxp.models import TipoDocumentoCxP,FacturaCompra,FacturaCompraDetalle
from compras.models import OrdenCompra
# Register your models here.

class TipoDocumentoCxPResource(resources.ModelResource):
    class Meta:
        model = TipoDocumentoCxP
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipo','descripcion','numeracion','caracteres','longitud','actual')        
        exclude = ('id',)

@ admin.register (TipoDocumentoCxP)
class TipoDocumentoCxP(ImportExportModelAdmin):
    list_display= ('idTipo','descripcion','numeracion','caracteres','longitud','actual')
    search_fields = ['descripcion']
    list_per_page = 30

class FacturaCompraResource(resources.ModelResource):
    class Meta:
        model = FacturaCompra
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','IdOrdenCompra','fecha','detalle','estado','IdTercero','IdSucursal','IdUsuario','valor','created','updated')        
        exclude = ('id',)

@ admin.register (FacturaCompra)
class FacturaCompra(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','IdOrdenCompra','fecha','detalle','estado','IdTercero','IdSucursal','IdUsuario','valor','created','updated')
    search_fields = ['IdTercero','IdOrdenCompra','detalle']
    list_per_page = 30

class FacturaCompraDetalleResource(resources.ModelResource):
    class Meta:
        model = FacturaCompraDetalle
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','IdFacturaCompra','estado','IdItem','valor','cantidad','valor_total','created','updated')        
        exclude = ('id',)

@ admin.register (FacturaCompraDetalle)
class FacturaCompraDetalle(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','IdFacturaCompra','estado','IdItem','valor','cantidad','valor_total','created','updated')
    search_fields = ['IdFacturaCompra','IdItem']
    list_per_page = 30
