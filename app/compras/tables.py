import django_tables2 as tables
from .models import OrdenCompra,OrdenCompraDetalle,Proveedor,Despacho,DetalleDespacho,ProveedorItem,EmpaqueItem
from inventarios.models import MaestroItem
from django.contrib.humanize.templatetags.humanize import intcomma
import django_tables2

class ColumnWithThousandsSeparator(django_tables2.Column):
    def render(self,value):
        return intcomma(value)

class OrdenCompraTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor  = ColumnWithThousandsSeparator()
    class Meta:
        model = OrdenCompra
        fields = ('numero','fecha','IdTipoDocumento','IdProveedor','despacho','detalle','estado','valor','IdSucursal' )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(6vh,0vh);" id="btnEditaOrdenCompra" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_orden_compra" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(6vh,0vh);" id="btnBorraOrdenCompra" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "confirma_borrado_orden_compra" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )            
    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(6vh,0vh);" id="btnDetalleOrdenCompra" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "detalle_orden_compra" id=record.id %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
     )    
    Nuevo_Item = tables.TemplateColumn(           
        '{% csrf_token %}'
        ''' <a style="transform: translate(6vh,0vh);" id="btnCreaDetalleOrden" type ="button" class="btn btn-warning" type="submit" href="{% url 'valida_crea_detalle_orden_compra' id=record.id %}" value="crea"><i <span class="material-icons">add</span</i></a>'''
    )     

    
class OrdenCompraDetalleTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor_unidad_empaque = ColumnWithThousandsSeparator()
    valor_compra = ColumnWithThousandsSeparator()
    valor_unitario = ColumnWithThousandsSeparator()
    cantidad_unidades_compra = ColumnWithThousandsSeparator()
    class Meta:
        model = OrdenCompraDetalle
        fields = ('numero','IdItem','cantidad_empaque','valor_unidad_empaque','cantidad_unidad_empaque','IdItem.IdUnidadMedida','cantidad_unidades_compra','IdItem.IdUnidadMedida','valor_compra','valor_unitario','IdItem.IdUnidadMedida')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(5vh,0vh);" style="transform: translate(10vh,0vh);" id="btnEditaOrdenCompraDetalle" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "valida_editar_orden_compra_detalle" id=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(5vh,0vh);" id="btnBorraOrdenCompraDetalle" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "confirma_borrado_orden_compra_detalle" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )

TEMPLATE1 = """
<input id="cantidad_empaque" maxlength="4" name="" type="text"/>
"""
TEMPLATE2 = """
<input id="valor_unidad_empaque" maxlength="5" name="Valor Unidad Empacado" type="text"/>
"""
TEMPLATE3 = """
<input id="cantidad_unidad_empaque" maxlength="5" name="" type="text"/>
"""
TEMPLATE4 = """
<input id="cantidad_unidades_compra" maxlength="5" name="" type="text"/>
"""
TEMPLATE5 = """
<input id="valor_compra" maxlength="5" name="" type="text"/>
"""
TEMPLATE6 = """
<input id="unidad_medida" maxlength="5" name="Unidad Medida" type="text"/>
"""
TEMPLATE6 = """
<input id="unidad_medida" maxlength="5" name="Unidad Medida" type="text"/>
"""

class ItemsOrdenListaTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    cantidad_empaque = tables.TemplateColumn(TEMPLATE1)
    unidad_medida = tables.TemplateColumn(TEMPLATE6)
    valor_unidad_empaque = tables.TemplateColumn(TEMPLATE2)
    cantidad_unidad_empaque = tables.TemplateColumn(TEMPLATE3)
    cantidad_unidades_compra = tables.TemplateColumn(TEMPLATE4)
    valor_compra = tables.TemplateColumn(TEMPLATE5)
    
    #valor_unidad_empaque = ColumnWithThousandsSeparator()
    #valor_compra = ColumnWithThousandsSeparator()
    class Meta:
        model = MaestroItem
        fields = ['descripcion']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelItem' type="button" class="btn btn-success btn-sm" type="submit" value="selecciona"><span class="material-icons">✔</span</a>''' 
    )                 

class ProveedoresListaTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Proveedor
        fields = ['identificacion','razon_social','apenom']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelTer' type="button" class="btn btn-success btn-sm" type="submit" href="{% url "crea_orden_compra" %}" value="selecciona"><span class="material-icons">✔</span</a>''' 
    )
    

class ProveedoresTable1(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Proveedor
        fields = ['identificacion','IdTipoIdentificacion','razon_social','apenom','direccion','telefono','email']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}    

    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnDetalleTercero" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "detalle_proveedor" id=record.id %}" value="detalle" ><i <span class="material-icons">menu</span</i></a>'''
     )    
    
class ProveedoresTable2(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Proveedor
        fields = ['IdPais','departamento','ciudad','contacto','por_ica','por_ret_fte','valor_debitos','valor_creditos','valor_saldo']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}    

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaTercero" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_proveedor" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraTercero" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_proveedor" pk=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )          

class DespachoTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    
    class Meta:
        model = Despacho
        fields = ('numero','fecha','IdTipoDocumento','IdOrdenCompra','IdProveedor','detalle','estado','IdSucursal' )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(5vh,0vh);" id="btnEditaDespacho" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_despacho" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )  
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(5vh,0vh);" id="btnBorraDespacho" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "confirma_borrado_despacho" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )            
    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(5vh,0vh);" id="btnDetalleDespacho" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "verifica_detalle_despacho" id=record.id %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
     )    
     
class DespachoDetalleTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    cantidad_enviada = tables.Column(
        attrs={"td": {"id": "cantidad_enviada"}})
    valor_total = tables.Column(
        attrs={"td": {"id": "valor_total"}})
    valor_total = ColumnWithThousandsSeparator()
    class Meta:
        model = DetalleDespacho
        fields = ('numero','IdItem','valor_unitario','cantidad_ordenada','cantidad_enviada','cantidad_unidad_empaque','cantidad_unidades_enviadas','IdItem.IdUnidadMedida','valor_total' )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<button style="transform: translate(7vh,0vh);" id="btnEditaDespachoDetalle" type="submit" data-toggle="modal" data-target="#" class="btn btn-success btn-sm" href="#"><span style="color:violet" class="material-icons">edit</span></button>'''
     )    
    """ Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(12vh,0vh);" id="btnBorraDespachoDetalle" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_despacho_detalle" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )     """
    
class OrdenCompraListaTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Proveedor
        fields = ['numero','IdProveedor','despacho']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelItem' type="button" class="btn btn-success btn-sm" type="submit" href="{% url "valida_crea_despacho" %}" value="selecciona"><span class="material-icons">✔</span</a>''' 
    ) 

class ProveedorItemTable(tables.Table):
    
    class Meta:
        model = ProveedorItem
        fields = ['IdProveedor','IdItem']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

class EmpaqueItemTable(tables.Table):
    
    class Meta:
        model = EmpaqueItem
        fields = ['IdItem','descripcion','cantidad']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}        