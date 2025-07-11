from django.contrib import admin
from import_export import fields,resources
from import_export.admin import ImportExportModelAdmin
from ventas.models import TipoDocumentoVenta,FormaPago,Cotizacion,CotizacionDetalle,FacturaVenta,FacturaVentaDetalle,NotaCredito
# Register your models here.

class TipoDocumentoVentaResource(resources.ModelResource):
    class Meta:
        model = TipoDocumentoVenta
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipo','descripcion','numeracion','caracteres','longitud','actual')        
        exclude = ('id',)

@ admin.register (TipoDocumentoVenta)
class TipoDocumentoVenta(ImportExportModelAdmin):
    list_display= ('idTipo','descripcion','numeracion','caracteres','longitud','actual')
    search_fields = ['descripcion']
    list_per_page = 30


class FormaPagoResource(resources.ModelResource):
    class Meta:
        model = FormaPago
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipo','descripcion','numeracion','caracteres','longitud','actual')        
        exclude = ('id',)

@ admin.register (FormaPago)
class FormaPago(ImportExportModelAdmin):
    list_display= ('idFormaPago','descripcion','credito')
    search_fields = ['descripcion']
    list_per_page = 30

class CotizacionResource(resources.ModelResource):
    class Meta:
        model = Cotizacion
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','idTipoDocumento','cliente','factura','fecha','detalle','estado','valor','IdSucursal','IdUsuario','created','updated')        
        exclude = ('id',)

@ admin.register (Cotizacion)
class Cotizacion(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','cliente','factura','fecha','detalle','estado','valor','IdSucursal','IdUsuario','created','updated')
    search_fields = ['cliente']
    list_per_page = 30


class CotizacionDetalleResource(resources.ModelResource):
    class Meta:
        model = CotizacionDetalle
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','IdItem','cantidad','valor_unit','valor_total','por_iva','por_desc','val_desc','valor_neto','estado','created','updated')        
        exclude = ('id',)

@ admin.register (CotizacionDetalle)
class CotizacionDetalle(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','IdItem','cantidad','valor_unit','valor_total','por_iva','por_desc','val_desc','valor_neto','estado','created','updated')
    search_fields = ['IdItem']
    list_per_page = 30


class FacturaVentaResource(resources.ModelResource):
    class Meta:
        model = FacturaVenta
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','IdTercero','forma_pago','fecha','detalle','estado','valor','IdSucursal','IdUsuario','created','updated')        
        exclude = ('id',)

@ admin.register (FacturaVenta)
class FacturaVenta(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','IdTercero','forma_pago','fecha','detalle','estado','valor','IdSucursal','IdUsuario','created','updated')
    search_fields = ['IdTercero','forma_pago']
    list_per_page = 30

class FacturaVentaDetalleResource(resources.ModelResource):
    class Meta:
        model = FacturaVentaDetalle
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','IdFactura','IdItem','cantidad','valor_unit','valor_total','por_iva','val_iva','por_desc','val_desc','valor_neto','estado','created','updated')        
        exclude = ('id',)

@ admin.register (FacturaVentaDetalle)
class FacturaVentaDetalle(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','IdFactura','IdItem','cantidad','valor_unit','valor_total','por_iva','val_iva','por_desc','val_desc','valor_neto','estado','created','updated')
    search_fields = ['IdTercero','forma_pago']
    list_per_page = 30

class NotaCreditoResource(resources.ModelResource):
    class Meta:
        model = NotaCredito
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocuemnto','IdTercero','fecha','detalle','valor','estado','IdSucursal','IdUsuario','created','updated')        
        exclude = ('id',)

