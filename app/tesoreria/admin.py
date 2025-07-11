from django.contrib import admin
from import_export import fields,resources
from import_export.admin import ImportExportModelAdmin
from tesoreria.models import TipoDocumentoTes,PagoProveedor,IngresoPagoCartera,Consignacion,Banco
# Register your models here.


class TipoDocumentoTesResource(resources.ModelResource):
    class Meta:
        model = TipoDocumentoTes
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipo','descripcion','numeracion','caracteres','longitud','actual')        
        exclude = ('id',)

@ admin.register (TipoDocumentoTes)
class TipoDocumentoTes(ImportExportModelAdmin):
    list_display= ('idTipo','descripcion','numeracion','caracteres','longitud','actual')
    search_fields = ['descripcion']
    list_per_page = 30


class BancoResource(resources.ModelResource):
    class Meta:
        model = Banco
        skip_unchanged = True
        report_skipped = True
        fields = ('idBanco','descripcion','sucursal','cuenta_no','telefonos','responsable','email_respons','debitos','creditos','saldo')        
        exclude = ('id',)

@ admin.register (Banco)
class Banco(ImportExportModelAdmin):
    list_display= ('idBanco','descripcion','sucursal','cuenta_no','telefonos','responsable','email_respons','debitos','creditos','saldo')
    search_fields = ['descripcion']
    list_per_page = 30


class PagoProveedorResource(resources.ModelResource):
    class Meta:
        model = PagoProveedor
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','fecha','detalle','estado','IdFacturaCompra','IdTercero','IdSucursal','IdUsuario','valor','created','updated')        
        exclude = ('id',)

@ admin.register (PagoProveedor)
class PagoProveedor(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','fecha','detalle','estado','IdFacturaCompra','IdTercero','IdSucursal','IdUsuario','valor','created','updated')
    search_fields = ['IdTercero','IdFacturaCompra']
    list_per_page = 30

class IngresoPagoCarteraResource(resources.ModelResource):
    class Meta:
        model = IngresoPagoCartera
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','fecha','detalle','estado','IdCartera','IdTercero','valor','IdUsuario','created','updated')        
        exclude = ('id',)

@ admin.register (IngresoPagoCartera)
class IngresoPagoCartera(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','fecha','detalle','estado','IdCartera','IdTercero','valor','IdUsuario','created','updated')
    search_fields = ['IdTercero','IdCartera']
    list_per_page = 30


class ConsignacionResource(resources.ModelResource):
    class Meta:
        model = Consignacion
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','fecha','detalle','estado','valor','IdBanco','IdUsuario','created','updated')        
        exclude = ('id',)

@ admin.register (Consignacion)
class Consignacion(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','fecha','detalle','estado','valor','IdBanco','IdUsuario','created','updated')
    search_fields = ['IdTercero','IdCartera']
    list_per_page = 30

