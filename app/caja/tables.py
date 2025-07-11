import django_tables2 as tables
from caja.models import ReciboCaja,ReciboCajaDetalle,PedidoCaja,PedidoCajaDetalle,PagoReciboCaja
import django_tables2
from django.contrib.humanize.templatetags.humanize import intcomma


class ColumnWithThousandsSeparator(django_tables2.Column):
    def render(self,value):
        return intcomma(value)
    
class RecibosCajaTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor = ColumnWithThousandsSeparator()
    class Meta:
        model = ReciboCaja
        fields = ("numero","fecha","detalle","IdTercero","IdMesa","IdHabitacion","IdCaja","pedido_caja","valor","pagado","IdUsuario" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnSelDet" type="button" class="btn btn-warning btn-sm" type="submit" href="{% url "recibo_caja_detalle" id=record.id %}" value="seleccionar" ><i <span class="material-icons">menu</span</i></a>'''
     )
    Pago = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnPagar" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "pago_recibo_caja" id=record.id %}" value="seleccionar" ><i <span class="material-icons">add</span</i></a>'''
     )
    PDF = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnImpresionReciboCaja" type="button" class="btn btn-primary" type="submit" href="{% url "impresion_recibo_caja_uno" id=record.id %}" value="seleccionar" ><i <span class="material-icons">print</span</i></a>'''
     )
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraReciboCaja" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrado_recibo_caja" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )
    
class RecibosCajaDetalleTable(tables.Table):
    valor = ColumnWithThousandsSeparator()
    valor_total = ColumnWithThousandsSeparator()
    class Meta:
        model = ReciboCajaDetalle
        fields = ("numero","pedido_caja","valor","IdItem","cantidad","valor_total")
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}


class PedidosCajaTable(tables.Table):
    valor_total = ColumnWithThousandsSeparator()
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    recibo_caja = tables.Column(
        attrs={"td": {"id": "recibo_caja"}})
    class Meta:
        model = PedidoCaja
        fields = ("numero","fecha","IdCaja","IdMesa","IdHabitacion","recibo_caja","IdUsuario","total_items","valor_total" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaPedidoCaja" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_pedido_caja" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaPedidoCaja" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrado_pedido_caja" record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )
    Adic_Items = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnAddItem" type="button" class="btn btn-primary btn-sm" type="submit" href="{% url "valida_adiciona_item_pedido_caja" id=record.id %}" value="seleccionar" ><i <span class="material-icons">add</span</i></a>'''
     )
    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnSelDet" type="button" class="btn btn-warning btn-sm" type="submit" href="{% url "detalle_pedido_caja" id=record.id %}" value="seleccionar" ><i <span class="material-icons">menu</span</i></a>'''
     )
    Recibo_Caja = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnReciboCaja" type="button" class="btn btn-info btn-sm" type="submit" href="{% url "busca_recibo_caja" id=record.id %}" value="cerrar" ><i <span class="material-icons">monetization_on</span</i></a>'''
     )

class PedidosCajaTableConsolidado(tables.Table):
    valor_total = ColumnWithThousandsSeparator()
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    recibo_caja = tables.Column(
        attrs={"td": {"id": "recibo_caja"}})
    class Meta:
        model = PedidoCaja
        fields = ("numero","fecha","IdCaja","IdMesa","IdHabitacion","recibo_caja","IdUsuario","total_items","valor_total" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaPedidoCaja" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_pedido_caja" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaPedidoCaja" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrado_pedido_caja" record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )
    Adic_Items = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnSelItem" type="button" class="btn btn-primary btn-sm" type="submit" href="{% url "valida_adiciona_item_pedido_caja" id=record.id %}" value="seleccionar" ><i <span class="material-icons">add</span</i></a>'''
     )
    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnSelDet" type="button" class="btn btn-warning btn-sm" type="submit" href="{% url "detalle_pedido_caja" id=record.id %}" value="seleccionar" ><i <span class="material-icons">menu</span</i></a>'''
     )
    """ Recibo_Caja = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnReciboCaja" type="button" class="btn btn-info btn-sm" type="submit" href="{% url "busca_recibo_caja" id=record.id %}" value="cerrar" ><i <span class="material-icons">monetization_on</span</i></a>'''
     ) """

""" class PedidosCajaTodosTable(tables.Table):
    valor_total = ColumnWithThousandsSeparator()
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = PedidoCaja
        fields = ("numero","fecha","IdCaja","IdMesa","IdHabitacion","recibo_caja","IdUsuario","total_items","valor_total" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaPedidoCaja" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_pedido_caja" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaPedidoCaja" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrado_pedido_caja" record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )
    Adic_Items = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnSelItem" type="button" class="btn btn-primary btn-sm" type="submit" href="{% url "selecciona_item_pedido_caja" id=record.id %}" value="seleccionar" ><i <span class="material-icons">add</span</i></a>'''
     )
    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnSelDet" type="button" class="btn btn-warning btn-sm" type="submit" href="{% url "detalle_pedido_caja" id=record.id %}" value="seleccionar" ><i <span class="material-icons">menu</span</i></a>'''
     )
    Recibo_Caja = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnSelPed" type="button" class="btn btn-info btn-sm" type="submit" href="{% url "busca_recibo_caja" id=record.id %}" value="cerrar" ><i <span class="material-icons">monetization_on</span</i></a>'''
     ) """
                
class PedidosCajaDetalleTable(tables.Table):
    valor = ColumnWithThousandsSeparator()
    valor_total = ColumnWithThousandsSeparator()
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = PedidoCajaDetalle
        fields = ("numero","IdItem","valor","cantidad","valor_total","created" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}            

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaDEtallePedidoCaja" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "valida_edita_item_pedido_caja" id=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraItemPedidoCaja" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrado_item_pedido_caja" id=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )

class PagosCajaTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor = ColumnWithThousandsSeparator()
    class Meta:
        model = PagoReciboCaja
        fields = ("numero","fecha","detalle","IdCaja","IdTercero","recibo_caja","IdTipoPago","IdTarjetaCredito","valor","IdUsuario" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}
    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraPago" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrado_pago_caja" id=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
    )

     

class CierreCajaTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor = ColumnWithThousandsSeparator()
    class Meta:
        model = PagoReciboCaja
        fields = ("numero","fecha","recibo_caja","IdCaja","IdTercero","IdTipoPago","IdTarjetaCredito","IdReciboCaja","valor","IdUsuario" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}    