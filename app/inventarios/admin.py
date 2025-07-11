
from django.contrib import admin
from import_export import fields,resources
from import_export.admin import ImportExportModelAdmin
from inventarios.models import TipoDocumentoInv,Grupo,SubGrupo,Medida,Bodega,MaestroItem,AcumuladoItem,Entrada,EntradaDetalle,Salida,SalidaDetalle,ProveedorItem,Kardex,InventarioFisico,CierreInventario,AjusteInventarioFisico,IngredienteProducto
# Register your models here.

class TipoDocumentoInvResource(resources.ModelResource):
    class Meta:
        model = TipoDocumentoInv
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipo','descripcion','numeracion','caracteres','longitud','actual')        
        exclude = ('id',)

@ admin.register (TipoDocumentoInv)
class TipoDocumentoInv(ImportExportModelAdmin):
    list_display= ('idTipo','descripcion','numeracion','caracteres','longitud','actual')
    search_fields = ['descripcion']
    list_per_page = 30

class GrupoResource(resources.ModelResource):
    class Meta:
        model = Grupo
        skip_unchanged = True
        report_skipped = True
        fields = ('descripcion')        
        exclude = ('id',)

@ admin.register (Grupo)
class Grupo(ImportExportModelAdmin):
    list_display= ('descripcion',)
    search_fields = ['descripcion']
    list_per_page = 30

class SubGrupoResource(resources.ModelResource):
    class Meta:
        model = SubGrupo
        skip_unchanged = True
        report_skipped = True
        fields = ('descripcion')        
        exclude = ('id',)

@ admin.register (SubGrupo)
class SubGrupo(ImportExportModelAdmin):
    list_display= ('descripcion',)
    search_fields = ['descripcion']
    list_per_page = 30

""" class MedidaResource(resources.ModelResource):
    class Meta:
        model = UnidadMedida
        skip_unchanged = True
        report_skipped = True
        fields = ('idMedida','descripcion')        
        exclude = ('id',)

@ admin.register (UnidadMedida)
class Medida(ImportExportModelAdmin):
    list_display= ('idMedida','descripcion')
    search_fields = ['descripcion']
    list_per_page = 30 """

class BodegaResource(resources.ModelResource):
    class Meta:
        model = Bodega
        skip_unchanged = True
        report_skipped = True
        fields = ('idBodega','descripcion','direccion','telefonos','responsable','email_bodega')        
        exclude = ('id',)

@ admin.register (Bodega)
class Bodega(ImportExportModelAdmin):
    list_display= ('idBodega','descripcion','direccion','telefonos','responsable','email_bodega')
    search_fields = ['descripcion']
    list_per_page = 30

class MaestroItemResource(resources.ModelResource):
    class Meta:
        model = MaestroItem
        skip_unchanged = True
        report_skipped = True
        fields = ('IdGrupo','IdSubGrupo','descripcion','IdUnidadMedida','marca','referencia_fabrica','valor_venta','valor_compra','por_iva','cant_maxima','cant_minima','costo_prom')        
        exclude = ('id',)

@ admin.register (MaestroItem)
class MaestroItem(ImportExportModelAdmin):
    list_display= ('IdGrupo','IdSubGrupo','descripcion','IdUnidadMedida','marca','referencia_fabrica','valor_venta','valor_compra','por_iva','cant_maxima','cant_minima','costo_prom')
    search_fields = ['IdGrupo','IdSubgrupo','descripcion']
    list_per_page = 30


class AcumuladoItemResource(resources.ModelResource):
    class Meta:
        model = AcumuladoItem
        skip_unchanged = True
        report_skipped = True
        fields = ('IdItem','anio','IdBodega','ii_01','ent_01','sal_01','if_01','ii_02','ent_02','sal_02','if_02','ii_03','ent_03','sal_03','if_03','ii_04','ent_04','sal_04','if_04','ii_05',
    'ent_05','sal_05','if_05','ii_06','ent_06','sal_06','if_06','ii_07','ent_07','sal_07','if_07','ii_08','ent_08','sal_08','if_08','ii_09','ent_09','sal_09','if_09','ii_10','ent_10','sal_10',
    'if_10','ii_11','ent_11','sal_11','if_11','ii_12','ent_12','sal_12','if_12')        
        exclude = ('id',)

@ admin.register (AcumuladoItem)
class AcumuladoItem(ImportExportModelAdmin):
    list_display= ('IdItem','anio','IdBodega','ii_01','ent_01','sal_01','if_01','ii_02','ent_02','sal_02','if_02','ii_03','ent_03','sal_03','if_03','ii_04','ent_04','sal_04','if_04','ii_05',
    'ent_05','sal_05','if_05','ii_06','ent_06','sal_06','if_06','ii_07','ent_07','sal_07','if_07','ii_08','ent_08','sal_08','if_08','ii_09','ent_09','sal_09','if_09','ii_10','ent_10','sal_10',
    'if_10','ii_11','ent_11','sal_11','if_11','ii_12','ent_12','sal_12','if_12')
    search_fields = ['IdItem','IdBodega']
    list_per_page = 30

class EntradaResource(resources.ModelResource):
    class Meta:
        model = Entrada
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','fecha','detalle','estado','IdTercero','factura_compra','orden_compra','IdUsuario','valor','created','updated')        
        exclude = ('id',)

@ admin.register (Entrada)
class Entrada(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','fecha','detalle','estado','IdProveedor','factura_compra','orden_compra','IdUsuario','valor','created','updated')
    search_fields = ['numero','fecha','IdTipoDocumento','IdTercero']
    list_per_page = 30

class EntradaDetalleResource(resources.ModelResource):
    class Meta:
        model = EntradaDetalle
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','IdEntrada','estado','IdItem','IdBodega','cantidad','valor','valor_total','created','updated')        
        exclude = ('id',)

@ admin.register (EntradaDetalle)
class EntradaDetalle(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','IdEntrada','estado','IdItem','IdBodega','cantidad','valor','valor_total','created','updated')
    search_fields = ['numero','IdTipoDocumento','IdItem']
    list_per_page = 30

class SalidaResource(resources.ModelResource):
    class Meta:
        model = Salida
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','fecha','detalle','estado','pedido_caja','IdUsuario','valor','created','updated')        
        exclude = ('id',)

@ admin.register (Salida)
class Salida(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','fecha','detalle','estado','pedido_caja','IdUsuario','valor','created','updated')
    search_fields = ['numero','IdTipoDocumento','IdTercero']
    list_per_page = 30


class SalidaDetalleResource(resources.ModelResource):
    class Meta:
        model = SalidaDetalle
        skip_unchanged = True
        report_skipped = True
        fields = ('numero','IdTipoDocumento','IdSalida','estado','IdItem','IdBodega','cantidad','valor','valor_total','created','updated')        
        exclude = ('id',)

@ admin.register (SalidaDetalle)
class SalidaDetalle(ImportExportModelAdmin):
    list_display= ('numero','IdTipoDocumento','IdSalida','estado','IdItem','IdBodega','cantidad','valor','valor_total','created','updated')
    search_fields = ['numero','IdTipoDocumento','IdItem']
    list_per_page = 30


class ProveedorItemResource(resources.ModelResource):
    class Meta:
        model = ProveedorItem
        skip_unchanged = True
        report_skipped = True
        fields = ('fecha','IdTercero','IdItem','IdOrdenCompra','valor','cantidad','valor_total')        
        exclude = ('id',)

@ admin.register (ProveedorItem)
class ProveedorItem(ImportExportModelAdmin):
    list_display= ('fecha','IdTercero','IdItem','IdOrdenCompra','valor','cantidad','valor_total')
    search_fields = ['fecha','IdTercero','IdItem','IdFacturaCompra','IdOrdenCompra']
    list_per_page = 30

class KardexResource(resources.ModelResource):
    class Kardex:
        model = Kardex
        skip_unchanged = True
        report_skipped = True
        fields = ('fecha','IdTercero','IdItem','IdOrdenCompra','valor','cantidad','valor_total')        
        exclude = ('id',)

@ admin.register (Kardex)
class kardex(ImportExportModelAdmin):
    list_display= ('fecha','IdTipoDocumento','pedido_caja','factura_compra','orden_compra','despacho','IdItem','valor','cantidad','valor_total','saldo','tipo_mov','IdBodega')
    search_fields = ['fecha','IdItem','pedido_caja','factura_compra','orden_compra','despacho','IdBodega']
    list_per_page = 30

class AjusteInventarioFisicoResource(resources.ModelResource):
    class Ajuste:
        model = AjusteInventarioFisico
        skip_unchanged = True
        report_skipped = True
        fields = ('IdAnio','IdMes','IdBodega')        
        exclude = ('id',)

@ admin.register (AjusteInventarioFisico)
class AjusteInventarioFisico(ImportExportModelAdmin):
    list_display= ('IdAnio','IdMes','IdBodega','numero_ajuste_entrada','numero_ajuste_salida')
    search_fields = ['fecha','IdBodega']
    list_per_page = 30

class InventarioFisicoResource(resources.ModelResource):
    class InventarioFisico:
        model = InventarioFisico
        skip_unchanged = True
        report_skipped = True
        fields = ('IdAnio','IdMes','inv_fis','inv_acum','diferencia','cerrado','IdBodega')        
        exclude = ('id',)

@ admin.register (InventarioFisico)
class InventarioFisico(ImportExportModelAdmin):
    list_display= ('IdAnio','IdMes','inv_fis','inv_acum','diferencia','numero_ajuste','cerrado','IdBodega')
    search_fields = ['fecha','IdBodega']
    list_per_page = 30

class MedidaResource(resources.ModelResource):
    class Medida:
        model = Medida
        skip_unchanged = True
        report_skipped = True
        fields = ('idMedida','descripcion',)        
        exclude = ('id',)

@ admin.register (Medida)
class Medida(ImportExportModelAdmin):
    list_display= ('idMedida','descripcion',)
    search_fields = ['idMedida','descripcion',]
    list_per_page = 30

class IngredienteProductoResource(resources.ModelResource):
    class IngredienteProducto:
        model = IngredienteProducto
        skip_unchanged = True
        report_skipped = True
        fields = ('producto','cantidad_necesaria')        
        exclude = ('id',)

@ admin.register (IngredienteProducto)
class IngredienteProducto(ImportExportModelAdmin):
    list_display= ('producto','cantidad_necesaria')
    search_fields = ['producto','cantidad_necesaria']
    list_per_page = 30