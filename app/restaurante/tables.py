import django_tables2 as tables
from restaurante.models import Mesa


class  MesasTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    
    class Meta:
        model = Mesa
        fields = ('idMesa','descripcion')
        #sequence = ('instance', 'name', )
        #template_name = 'django_tables2/semantic.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelMesa' type="button" type="submit" href="{% url "crea_pedido_caja_mesa" id=record.id %}" value="quita" style="color:red">✔</a>'''
    )