from django.contrib import admin
from import_export import fields,resources
from import_export.admin import ImportExportModelAdmin
from caja.models import Caja,TipoDocumentoCaja,TipoEgresoCaja,ReciboCaja,ReciboCajaDetalle,EgresoCaja,PedidoCaja,PedidoCajaDetalle,TipoIngresoCaja,TipoPagoReciboCaja,TarjetaCredito,PagoReciboCaja
# Register your models here.

class PedidoCajaResource(resources.ModelResource):
    class Meta:
        model = PedidoCaja
        skip_unchanged = True
        report_skipped = True
        fields = ("fecha", "numero","IdTipoIngreso","IdCaja","IdMesa","IdHabitacion","recibo_caja")        
        exclude = ('id',)

@ admin.register (PedidoCaja)
class PedidoCaja(ImportExportModelAdmin):
    list_display= ("fecha", "numero","IdTipoIngreso","IdCaja","IdMesa","IdHabitacion","recibo_caja")
    search_fields = ['descripcion']
    list_per_page = 30

class PedidoCajaDetalleResource(resources.ModelResource):
    class Meta:
        model = PedidoCajaDetalle
        skip_unchanged = True
        report_skipped = True
        fields = ("numero","IdTipoDocumento","IdPedidoCaja","IdItem","valor","cantidad","valor_total")        
        exclude = ('id',)

@ admin.register (PedidoCajaDetalle)
class PedidoCajaDetalle(ImportExportModelAdmin):
    list_display= ("numero","IdTipoDocumento","IdPedidoCaja","IdItem","valor","cantidad","valor_total")
    search_fields = ['descripcion']
    list_per_page = 30

#class PedidoCajaAdmin(admin.ModelAdmin):
#    fields = ["fecha", "numero","IdTipoIngreso","IdCaja","IdMesa","IdHabitacion","recibo_caja"]
#admin.site.register(PedidoCaja, PedidoCajaAdmin)

#class PedidoCajaDetalleAdmin(admin.ModelAdmin):
#    fields = ["numero",]
#admin.site.register(PedidoCajaDetalle, PedidoCajaDetalleAdmin)

class TipoDocumentoCajaResource(resources.ModelResource):
    class Meta:
        model = TipoDocumentoCaja
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipo','descripcion','numeracion','caracteres','longitud','actual')        
        exclude = ('id',)

@ admin.register (TipoDocumentoCaja)
class TipoDocumentoCaja(ImportExportModelAdmin):
    list_display= ('idTipo','descripcion','numeracion','caracteres','longitud','actual')
    search_fields = ['descripcion']
    list_per_page = 30

class CajaResourceResorce(resources.ModelResource):
    class Meta:
        model = Caja
        skip_unchanged = True
        report_skipped = True
        fields = ('idCaja','valor_base','descripcion','consolidada')        
        exclude = ('id',)

@ admin.register (Caja)
class Caja(ImportExportModelAdmin):
    list_display= ('idCaja','valor_base','descripcion','consolidada')
    search_fields = ['descripcion']
    list_per_page = 30

class TipoEgresoCajaResource(resources.ModelResource):
    class Meta:
        model = TipoEgresoCaja
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipoEgreso','descripcion')        
        exclude = ('id',)

@ admin.register (TipoEgresoCaja)
class TipoEgresoCaja(ImportExportModelAdmin):
    list_display= ('idTipoEgreso','descripcion')
    search_fields = ['descripcion']
    list_per_page = 30

class TipoIngresoCajaResource(resources.ModelResource):
    class Meta:
        model = TipoIngresoCaja
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipoIngreso','descripcion')        
        exclude = ('id',)

@ admin.register (TipoIngresoCaja)
class TipoIngresoCaja(ImportExportModelAdmin):
    list_display= ('idTipoIngreso','descripcion')
    search_fields = ['descripcion']
    list_per_page = 30


class ReciboCajaResource(resources.ModelResource):
    class Meta:
        model = ReciboCaja 
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','fecha','detalle','estado','IdCaja','IdTercero','valor','IdSucursal','IdUsuario','created','updated')        
        exclude = ('id',)

@ admin.register (ReciboCaja)
class ReciboCaja(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','fecha','detalle','pagado','IdCaja','IdTercero','valor','IdSucursal','IdUsuario','created','updated')
    search_fields = ['detalle']
    list_per_page = 30

class ReciboCajaDetalleResource(resources.ModelResource):
    class Meta:
        model = ReciboCajaDetalle 
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','IdReciboCaja','IdItem','valor','cantidad','valor_total','created','updated')        
        exclude = ('id',)

@ admin.register (ReciboCajaDetalle)
class ReciboCajaDetalle(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','IdReciboCaja','valor','IdItem','valor','cantidad','valor_total','created','updated')
    search_fields = ['numero',]
    list_per_page = 30


class EgresoCajaResource(resources.ModelResource):
    class Meta:
        model = EgresoCaja 
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','IdTipoEgreso','fecha','detalle','estado','IdCaja','valor','IdSucursal','IdUsuario','created','updated')        
        exclude = ('id',)

@ admin.register (EgresoCaja)
class EgresoCaja(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','IdTipoEgreso','fecha','detalle','estado','IdCaja','valor','IdSucursal','IdUsuario','created','updated')
    search_fields = ['numero','IdCaja']
    list_per_page = 30


@ admin.register (TipoPagoReciboCaja)
class TipoPagoReciboCaja(ImportExportModelAdmin):
    list_display= ('descripcion',)
    search_fields = ['descripcion',]
    list_per_page = 30

@ admin.register (TarjetaCredito)
class TarjetaCredito(ImportExportModelAdmin):
    list_display= ('descripcion',)
    search_fields = ['descripcion',]
    list_per_page = 30

@ admin.register (PagoReciboCaja)
class PagoReciboCaja(ImportExportModelAdmin):
    list_display= ('numero','fecha','IdTipoPago',"IdTercero","recibo_caja",'IdTarjetaCredito','detalle','valor','IdSucursal','IdUsuario','created','updated')
    search_fields = ['descripcion',]
    list_per_page = 30
	
