from django.contrib import admin
from import_export import fields,resources
from import_export.admin import ImportExportModelAdmin
from compras.models import TipoDocumentoCompra,OrdenCompra,OrdenCompraDetalle,DetalleDespacho,Despacho,Proveedor,EmpaqueItem


class TipoDocumentoCajaResource(resources.ModelResource):
    class Meta:
        model = TipoDocumentoCompra
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipo','descripcion','numeracion','caracteres','longitud','actual')        
        exclude = ('id',)

@ admin.register (TipoDocumentoCompra)

class TipoDocumentoCaja(ImportExportModelAdmin):
    list_display= ('idTipo','descripcion','numeracion','caracteres','longitud','actual')
    search_fields = ['idTipo','descripcion']
    list_per_page = 30


class ProveedorResource(resources.ModelResource):
    class Meta:
        model = Proveedor
        skip_unchanged = True
        report_skipped = True
        fields = ('identificacion','IdTipoIdentificacion','nombre1','nombre2','apel1','apel2','apenom','razon_social','direccion','telefono',
                  'email','IdPais','departamento','ciudad','contacto','IdUsuario','por_ica','por_ret_fte','valor_debitos','valor_creditos','valor_saldo')        
        exclude = ('id',)

@ admin.register (Proveedor)
class Proveedor(ImportExportModelAdmin):
    list_display= ('identificacion','IdTipoIdentificacion','nombre1','nombre2','apel1','apel2','apenom','razon_social','direccion','telefono',
                  'email','IdPais','departamento','ciudad','contacto','IdUsuario','por_ica','por_ret_fte','valor_debitos','valor_creditos','valor_saldo')
    search_fields = ['identificacion','apenom','razon_social']
    list_per_page = 30


class OrdenCompraResouce(resources.ModelResource):
    class Meta:
        model = OrdenCompra
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','fecha','IdProveedor','detalle','estado','IdSucursal','IdUsuario','created','updated')        
        exclude = ('id',)

@ admin.register (OrdenCompra)
class OrdenCompra(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','fecha','IdProveedor','detalle','estado','IdSucursal','IdUsuario','created','updated')
    search_fields = ['numero','IdProveedor']
    list_per_page = 30

class OrdenCompraDetalleResource(resources.ModelResource):
    class Meta:
        model = OrdenCompraDetalle
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','estado','IdItem','valor_compra','cantidad_unidad_empaque','cantidad_empaque','cantidad_unidades_compra','valor_unitario','created','updated')        
        exclude = ('id',)

@ admin.register (OrdenCompraDetalle)
class OrdenCompraDetalle(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','estado','IdItem','valor_compra','cantidad_unidad_empaque','valor_unidad_empaque','cantidad_empaque','cantidad_unidades_compra','valor_unitario','created','updated')
    search_fields = ['numero','IdItem']
    list_per_page = 30


class DespachoResource(resources.ModelResource):
    class Meta:
        model = Despacho
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','estado','IdItem','valor_compra','cantidad_unidad_empaque','valor_unidad_empaque','cantidad_empaque','cantidad_unidades_compra','valor_unitario','created','updated')    
        exclude = ('id',)

@ admin.register (Despacho)
class Despacho(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','fecha','IdProveedor','IdOrdenCompra','detalle','estado','IdSucursal','IdUsuario','created','updated')
    search_fields = ['numero','IdOrdenCompra']
    list_per_page = 30

	
class DetalleDespachoResouce(resources.ModelResource):
    class Meta:
        model = DetalleDespacho
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdDespacho','estado','IdItem','valor_unitario','cantidad_ordenada','cantidad_enviada','cantidad_unidad_empaque','cantidad_unidades_enviadas','valor_total','created','updated')        
        exclude = ('id',)

@ admin.register (DetalleDespacho)
class DetalleDespacho(ImportExportModelAdmin):
    list_display= ('numero','IdDespacho','estado','IdItem','valor_unitario','cantidad_ordenada','cantidad_enviada','cantidad_unidad_empaque','cantidad_unidades_enviadas','valor_total','created','updated')
    search_fields = ['numero','IdItem']
    list_per_page = 30

class EmpaqueItemResouce(resources.ModelResource):
    class Meta:
        model = EmpaqueItem
        skip_unchanged = True
        report_skipped = True
        fields = ('IdItem','descripcion','cantidad')        
        exclude = ('id',)

@ admin.register (EmpaqueItem)
class EmpaqueItem(ImportExportModelAdmin):
    list_display= ('IdItem','descripcion','cantidad')
    search_fields = ['IdItem','descripcion']
    list_per_page = 30

