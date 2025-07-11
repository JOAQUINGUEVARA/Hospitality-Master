import django_tables2 as tables
from core.models import Tercero


class TercerosListaTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Tercero
        fields = ['identificacion','apenom','razon_social']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelTer' type="button" class="btn btn-success btn-sm" type="submit" href="{% url "crea_recibo_caja" %}" value="selecciona"><span class="material-icons">✔</span</a>''' 
    )
    """ Crear = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnCreaTer' type="button" class="btn btn-info btn-sm" type="submit" href="{% url "crea_tercero_cierre_pedido_caja" id=1 %}" value="crea"><span class="material-icons">add</span</a>''' 
    ) """

class TercerosRegistroTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Tercero
        fields = ['identificacion','apenom','razon_social']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelTer' type="button" class="btn btn-success btn-sm" type="submit" href="{% url "crea_registro" %}" value="selecciona"><span class="material-icons">✔</span</a>''' 
    )

class TercerosLista1Table(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Tercero
        fields = ['identificacion','apenom','razon_social']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelTer' type="button" class="btn btn-success btn-sm" type="submit" href="{% url "recibo_caja_consolidado" record.id %}" value="selecciona"><span class="material-icons">✔</span</a>''' 
    )
    """ Crear = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnCreaTer' type="button" class="btn btn-info btn-sm" type="submit" href="{% url "crea_tercero_cierre_pedido_caja" id=2 %}" value="crea"><span class="material-icons">add</span</a>''' 
    ) """

class TercerosTable1(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Tercero
        fields = ['identificacion','IdTipoIdentificacion','identifica_de','IdTipoTercero','nombre1','nombre2','apel1','apel2','razon_social','nombre','direccion','telefono','email','ocupacion']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}    

    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnDetalleTercero" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "detalle_tercero" id=record.id %}" value="detalle" ><i <span class="material-icons">menu</span</i></a>'''
     )    
    
class TercerosTable2(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Tercero
        fields = ['IdPais','departamento','ciudad','contacto','por_ica','por_ret_fte','valor_debitos','valor_creditos','valor_saldo']
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}    

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaTercero" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_tercero" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraTercero" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_tercero" pk=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )      