import django_tables2 as tables
from inventarios.models import MaestroItem
from django.contrib.humanize.templatetags.humanize import intcomma
import django_tables2
from .models import Receta, Ingrediente,RecetaIngrediente,OrdenProduccion,OrdenProduccionIngrediente

class ColumnWithThousandsSeparator(django_tables2.Column):
    def render(self,value):
        return intcomma(value)
    
class IngredienteTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Ingrediente
        fields = ("ingrediente","unidad_medida","cantidad_stock")  
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}
       
    """ Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(8vh,0vh);"  id="btnEditaItemReceta" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "editar_item_receta" id=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     ) """    
    """ Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(8vh,0vh);" id="btnBorraItemReceta" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borrar_item_receta" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     ) """

class RecetaTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = Receta
        fields = ("producto",)
        
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}
       
    Ingredientes = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnIngredienteReceta" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "receta_ingredientes_lista" id=record.id %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
     )
    Adic_Ingrediente = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnAddIngrediente" type="button" class="btn btn-warning" type="submit" href="{% url "crea_ingrediente_receta" pk=record.id %}" value="editar" ><i <span class="material-icons">add</span</i></a>'''
    )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(8vh,0vh);" id="btnBorraReceta" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_receta" pk=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )
         
class RecetaIngredienteTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = RecetaIngrediente
        fields = ("ingrediente","cantidad_necesaria","ingrediente.unidad_medida")
        
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"} 
    
    """ Adic_Ingrediente = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnAddIngrediente" type="button" class="btn btn-warning" type="submit" href="{% url "crea_ingrediente_receta" pk=idreceta %}" value="editar" ><i <span class="material-icons">menu</span</i></a>'''
    ) """
    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(3vh,0vh);"  id="btnEditaIngedienteReceta" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_ingrediente_receta" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
    )    
    Borrar_Ingrediente = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(8vh,0vh);" id="btnBorraIngredienteReceta pk=record.id" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_ingrediente_receta" pk=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )     
    
""" class RecetaIngredienteTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = RecetaIngrediente
        fields = ("ingrediente","cantidad_necesaria")
        
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}      """

class OrdenProduccionTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    costo_orden = ColumnWithThousandsSeparator()
    class Meta:
        model = OrdenProduccion
        fields = ("numero","fecha","receta","cantidad_producir","costo_orden","estado")
        
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}
       
    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a style="transform: translate(1vh,0vh);"  id="btnEditaOrdenProduccion" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "valida_edita_orden_produccion" id=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
    )
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(1vh,0vh);" id="btnBorraOrdenProduccion" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_orden_produccion" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )
    Cargar_Ing_Receta = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(5vh,0vh);" id="btnCargaItemsOrdenProduccion" type="button" class="btn btn-warning btn-sm" type="submit" href="{% url "valida_carga_items_orden_produccion" id=record.id %}" value="editar" ><i <span class="material-icons">add</span</i></a>'''
     ) 
    Ingredientes = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(4vh,0vh);" id="btnItemsOrdenProduccion" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "orden_produccion_detalle" id=record.id %}" value="ver" ><i <span class="material-icons">menu</span</i></a>'''
     )
    Ejecutar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(1vh,0vh);" id="btnEjecutaOrdenProduccion" type="button" class="btn btn-warning btn-sm" type="submit" href="{% url "ejecuta_orden_produccion" id=record.id %}" value="editar" ><i <span class="material-icons">add</span</i></a>'''
     )
    Aplicar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(1vh,0vh);" id="btnAplicaOrdenProduccion" type="button" class="btn btn btn-dark " type="submit" href="{% url "aplica_orden_produccion" id=record.id %}" value="editar" ><i <span class="material-icons">undo</span</i></a>'''
     )
     
class OrdenProduccionIngredienteTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    precio_compra_unitario = ColumnWithThousandsSeparator()
    cantidad_stock = ColumnWithThousandsSeparator()
    costo_compra = ColumnWithThousandsSeparator()
    cantidad_a_comprar = ColumnWithThousandsSeparator()
    class Meta:
        model = OrdenProduccionIngrediente
        attrs = {'class': 'paleblue','width':'80%'}
        fields = ("ingrediente","cantidad_necesaria","cantidad_stock","cantidad_a_comprar","precio_compra_unitario","costo_compra")
        
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}
    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(3vh,0vh);" id="btnBorraItemOrdenProduccion" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrado_ingrediente_orden_produccion" id=record.id %}" value="borra" ><i <span class="material-icons">delete</span</i></a>'''
     )
    """ Ad_Ingrediente = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a  style="transform: translate(8vh,0vh);" id="btnCargaItemsOrdenProduccion" type="button" class="btn btn-warning btn-sm" type="submit" href="{% url "" %}" value="add" ><i <span class="material-icons">add</span</i></a>'''
     )
         """
