import django_tables2 as tables
from inventarios.models import MaestroItem,Grupo,SubGrupo,Bodega,Medida,AcumuladoItem,Salida,SalidaDetalle,Entrada,EntradaDetalle,Kardex,InventarioFisico
from django.contrib.humanize.templatetags.humanize import intcomma
import django_tables2

class ColumnWithThousandsSeparator(django_tables2.Column):
    def render(self,value):
        return intcomma(value)

TEMPLATE1 = """
<input id="cantidad" maxlength="7" name="cantidad" type="text"/>
"""
TEMPLATE2 = """
<input id="valor" maxlength="7" name="valor" type="text"/>
"""

TEMPLATE3 = """
<input id="valor_total" maxlength="7" name="valor_total" type="text"/>
"""

class ItemsListaTable1(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    cantidad = tables.TemplateColumn(TEMPLATE1)
    #valor = tables.TemplateColumn(TEMPLATE2)
    #valor_venta = ColumnWithThousandsSeparator()
    class Meta:
        model = MaestroItem
        fields = ['descripcion']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelItem' type="button" class="btn btn-success btn-sm" type="submit" value="selecciona"><span class="material-icons">✔</span</a>''' 
    )

class ItemsListaTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    cantidad = tables.TemplateColumn(TEMPLATE1)
    valor = tables.TemplateColumn(TEMPLATE2)
    valor_venta = ColumnWithThousandsSeparator()
    class Meta:
        model = MaestroItem
        fields = ['descripcion','valor_venta']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelItem' type="button" class="btn btn-success btn-sm" type="submit" value="selecciona"><span class="material-icons">✔</span</a>''' 
    )

class ItemsListaPedidoTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    cantidad = tables.TemplateColumn(TEMPLATE1)
    class Meta:
        model = MaestroItem
        fields = ['descripcion']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelItem' type="button" class="btn btn-success btn-sm" type="submit" value="selecciona"><span class="material-icons">✔</span</a>''' 
    )

class GruposInventarioTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Grupo
        fields = ("descripcion","IdBodega" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaGrupoInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_grupo_inventario" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraGrupoInventario" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_grupo_inventario" pk=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )
    

class SubGruposInventarioTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = SubGrupo
        fields = ("IdGrupo","descripcion",)
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaSubGrupoInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_sub_grupo_inventario" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraSubGrupoInventario" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_sub_grupo_inventario" pk=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )    
    
class BodegasInventarioTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Bodega
        fields = ("idBodega","descripcion","direccion","telefonos","responsable")
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaGrupoInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_bodega_inventario" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraGrupoInventario" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_bodega_inventario" pk=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )    
class ItemsInventarioTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = MaestroItem
        fields = ("IdGrupo","IdSubGrupo","descripcion","tipo_producto","IdUnidadMedida","marca","referencia_fabrica","IdBodega")
        
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaItemInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "detalle_item_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
     )
    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaItemInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_item_inventario" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraItemInventario" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_item_inventario" pk=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )
         
class ItemsInventarioTable1(tables.Table):
    
    class Meta:
        model = MaestroItem
        fields = ("IdGrupo","IdSubGrupo","descripcion","IdUnidadMedida","marca","referencia_fabrica","IdBodega")
        
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    
    """ Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaItemInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "detalle_item_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
     ) """
    """ Acumulado = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnAcumuladoItemInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "detalle_acumulado_item_inventario" id=record.id idbodega=record.IdBodega_id %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
     )        """
        
class ItemsInventarioTable2(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor_venta = ColumnWithThousandsSeparator()
    valor_compra = ColumnWithThousandsSeparator()
    costo_prom = ColumnWithThousandsSeparator()
    class Meta:
        model = MaestroItem
        fields = ("valor_venta","valor_compra","tipo_producto","por_iva","cant_maxima","cant_minima","costo_prom","acumula")
        
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaItemInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_item_inventario" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraItemInventario" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_item_inventario" pk=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )        
    

class MedidasInventarioTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Medida
        fields = ("idMedida","descripcion" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaMedidaInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_medida_inventario" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraMedidaInventario" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_medida_inventario" pk=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )    

class AcumuladoItemsInventarioTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    costo_prom = ColumnWithThousandsSeparator()
    class Meta:
        model = AcumuladoItem
        fields = ("IdItem","IdBodega","costo_prom","if_12")
     
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnDetalleItemInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "detalle_acumulado_item_inventario" id=record.id idbodega=record.IdBodega_id %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
     )

class AcumuladoItemsInventarioTable1(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = AcumuladoItem
        fields = ("IdItem","IdBodega","IdItem.IdUnidadMedida")
     
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnDetalleItemInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "detalle_acumulado_item_inventario" id=record.id idbodega=record.IdBodega_id %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
     )
    
class AcumuladoItemsInventarioTable2(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = AcumuladoItem
        fields = ("IdBodega","anio","ii_01","ent_01","sal_01","if_01","ii_02","ent_02","sal_02","if_02","ii_03","ent_03","sal_03","if_03",
                  "ii_04","ent_04","sal_04","if_04","ii_05","ent_05","sal_05","if_05","ii_06","ent_06","sal_06","if_06","ii_07","ent_07","sal_07","if_07")
     
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}


class AcumuladoItemsInventarioTable3(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = AcumuladoItem
        fields = ("IdBodega","anio","ii_08","ent_08","sal_08","if_08","ii_09","ent_09","sal_09","if_09","ii_10","ent_10","sal_10","if_10","ii_11","ent_11","sal_11","if_11",
                  "ii_12","ent_12","sal_12","if_12")
     
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}


class AcumuladoItemsInventarioTable4(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    costo_prom = ColumnWithThousandsSeparator()
    class Meta:
        model = AcumuladoItem
        fields = ("IdBodega","cant_maxima","cant_minima","costo_prom")
     
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}    

class SalidasInventarioTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor = ColumnWithThousandsSeparator()
    class Meta:
        model = Salida
        fields = ('numero','fecha','anio','IdTipoDocumento','pedido_caja','detalle','valor')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(8vh,0vh);"  id="btnEditaSalidaInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "valida_editar_salida_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(8vh,0vh);" id="btnBorraSalidaInventario" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrar_salida_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )            
    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(8vh,0vh);" id="btnDetalleSalidaInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "verifica_detalle_salida_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
     )    
    Nuevo_Item = tables.TemplateColumn(           
        '{% csrf_token %}'
        ''' <a style="transform: translate(10vh,0vh);" id="btnCreaDetalleSalida" type ="button" class="btn btn-warning" type="submit" href="{% url 'crea_detalle_salida_inventario' id=record.id %}" value="crea"><i <span class="material-icons">add</span</i></a>'''
    )  

class SalidasInventarioDetalleTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor = ColumnWithThousandsSeparator()
    valor_total = ColumnWithThousandsSeparator()
    class Meta:
        model = SalidaDetalle
        fields = ('numero','IdItem','IdBodega','valor','cantidad','valor_total','estado' )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(15vh,0vh);" id="btnEditaSalidaDetalleInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "valida_editar_detalle_salida_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(15vh,0vh);" id="btnBorraSalidaDetalleInventario" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrar_salida_detalle_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )
              

class EntradasInventarioTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor  = ColumnWithThousandsSeparator()
    class Meta:
        model = Entrada
        fields = ('numero','fecha','anio','IdTipoDocumento','orden_compra','despacho','factura_compra','detalle','valor','IdUsuario' )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(7vh,0vh);" id="btnEditaEntradaInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "valida_editar_entrada_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(7vh,0vh);" id="btnBorraEntradaInventario" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrar_entrada_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )            
    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(7vh,0vh);" id="btnDetalleEntradaInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "verifica_detalle_entrada_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
     )    
    Nuevo_Item = tables.TemplateColumn(           
        '{% csrf_token %}'
        ''' <a style="transform: translate(7vh,0vh);" id="btnCreaDetalleSalida" type ="button" class="btn btn-warning" type="submit" href="{% url 'crea_detalle_entrada_inventario' id=record.id %}" value="crea"><i <span class="material-icons">add</span</i></a>'''
    )     

class EntradasInventarioDetalleTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor = ColumnWithThousandsSeparator()
    valor_total = ColumnWithThousandsSeparator()
    class Meta:
        model = EntradaDetalle
        fields = ('numero','IdItem','IdBodega','valor','cantidad','valor_total' )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(10vh,0vh);"  id="btnEditaEntradaDetalleInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "valida_editar_entrada_detalle_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(10vh,0vh);" id="btnBorraEntradaDetalleInventario" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrar_entrada_detalle_inventario" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )
    """ Nuevo_Item = tables.TemplateColumn(           
        '{% csrf_token %}'
        ''' <a style="transform: translate(18vh,0vh);" id="btnCreaDetalleSalida" type ="button" class="btn btn-warning" type="submit" href="{% url 'crea_detalle_entrada_inventario' id=record.IdEntrada_id %}" value="crea"><i <span class="material-icons">add</span</i></a>'''
    )    """         

class KardexTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = MaestroItem
        fields = ("idItem","descripcion")
     
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Kardex = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnKardexItemInventario" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "kardex_detalle" id=record.id %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
     )    
    
class KardexItemTable(tables.Table):
    valor = ColumnWithThousandsSeparator()
    valor_total = ColumnWithThousandsSeparator()
    class Meta:
        model = Kardex
        fields = ("fecha","numero","IdTipoDocumento","tipo_mov","factura_compra","orden_compra","despacho","pedido_caja","valor","cantidad","valor_total","saldo")
     
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

class InventarioFisicoTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = InventarioFisico
        fields = ("IdItem","inv_fis","inv_acum","diferencia")
     
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(1vh,0vh);" style="transform: translate(1vh,0vh);" id="btnEditaInventarioFisico" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_inventario_fisico" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )           


class ItemsInventarioFisicoTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    cantidad = tables.TemplateColumn(TEMPLATE1)
    class Meta:
        model = MaestroItem
        fields = ['descripcion']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelItem' type="button" class="btn btn-success btn-sm" type="submit" value="selecciona"><span class="material-icons">✔</span</a>''' 
    )
