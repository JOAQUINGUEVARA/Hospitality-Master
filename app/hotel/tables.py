import django_tables2 as tables
from hotel.models import Habitacion,TipoHabitacion,ReservaHabitacion,RegistroHotel,AcompañanteHotel
from caja.models import PedidoCaja,PedidoCajaDetalle,ReciboCaja,ReciboCajaDetalle,PagoReciboCaja
from django.contrib.humanize.templatetags.humanize import intcomma

class ColumnWithThousandsSeparator(tables.Column):
    def render(self,value):
        return intcomma(value)

class  TipoHabitacionTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    
    class Meta:
        model = TipoHabitacion
        fields = ('idTipoHabitacion','descripcion')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaTipoHabitacion" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_tipos_habitacion" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraTipoHabitacion" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_tipos_habitacion" pk=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )
    

class  HabitacionesTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    
    class Meta:
        model = Habitacion
        fields = ('idHabitacion','descripcion')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelHabitacion' type="button" type="submit" href="{% url "crea_pedido_caja_habitacion" id=record.id %}" value="selecciona" style="color:red">✔</a>'''
     )

class  HabitacionesConsolidadoTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    
    class Meta:
        model = Habitacion
        fields = ('idHabitacion','descripcion')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Seleccionar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id='BtnSelHabitacion' type="button" type="submit" href="{% url "pedidos_caja_consolidados" id=record.id %}" value="selecciona" style="color:red">✔</a>'''
     )

class  Habitaciones1Table(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    
    class Meta:
        model = Habitacion
        fields = ('idHabitacion','IdTipoHabitacion','descripcion','valor_noche','ocupada')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaTipoHabitacion" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_habitacion" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraTipoHabitacion" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_habitacion" pk=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )
    
class  ReservasTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor_reserva = ColumnWithThousandsSeparator()
    class Meta:
        model = ReservaHabitacion
        fields = ('IdHabitacion','nombre_reserva','fecha_reserva','fecha_ingreso','fecha_salida','no_de_noches')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}
    
    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaReserva" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "reservas_detalle_list" id=record.id %}" value="detalle" ><i <span class="material-icons">menu</span</i></a>'''
     )        
    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaReserva" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_reserva" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraReserva" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_reserva" pk=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )

class  ReservasTable1(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor_reserva = ColumnWithThousandsSeparator()
    class Meta:
        model = ReservaHabitacion
        fields = ('consecutivo','descripcion','valor_reserva','telefono','email','pin')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}
            
class  RegistrosTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor_pago = ColumnWithThousandsSeparator()
    class Meta:
        model = RegistroHotel
        fields = ('consecutivo','IdHabitacion','IdTercero','check_in','hora_check_in','check_out','hora_check_out','no_de_noches','valor_pago','pagado')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}
    
    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnDetalleRegistro" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "registro_detalle_list" id=record.id %}" value="detalle" ><i <span class="material-icons">menu</span</i></a>'''
     )
    Pedidos = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnPedidos" type="button" class="btn btn-secondary btn-sm" type="submit" href="{% url "registro_pedidos_caja_consolidado" id=record.id %} " value="detalle" ><i <span class="material-icons">switch_account</span</i></a>'''
     )
    Check_Out = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnCheckOut" type="button" class="btn btn-warning btn-sm" type="submit" href="{% url "check_out" pk=record.id %}" value="detalle" ><i <span class="material-icons">check_box</span</i></a>'''
     )
    Liq_Estadía = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnLiquida" type="button" class="btn btn-dark btn-sm" type="submit" href="{% url "liquida_estadia" pk=record.id %}" value="detalle" ><i <span class="material-icons">payments</span</i></a>'''
     )
    ReciboCaja = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnReciboCaja" type="button" class="btn btn-info btn-sm" type="submit" href="{% url "valida_creacion_recibo_caja_estadia" %}" value="detalle" ><i <span class="material-icons">price_check</span</i></a>'''
     )  
    Tercero = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnTercero" type="button" class="btn btn-light btn-sm" type="submit" href="{% url "tercero_edit" id=record.id %}" value="detalle" ><i <span class="material-icons">group</span</i></a>'''
     )
    Acomp_Reg = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnAcompañante" type="button" class="btn btn-dark btn-sm" type="submit" href="{% url "acompañante_hotel_list" id=record.id %}" value="detalle" ><i <span class="material-icons">group</span</i></a>'''
     )            
    Formato_Reg = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnFormatoRegistro" type="button" class="btn btn-info btn-sm" type="submit" href="{% url "impresion_formato_registro" id=record.id %}" value="detalle" ><i <span class="material-icons">print</span</i></a>'''
     )
    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaRegistro" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_registro" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    """ Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraRegistro" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_acompañante_hotel" pk=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )   """  

class  RegistrosTable1(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = RegistroHotel
        fields = ('consecutivo','descripcion','tarifa_habitacion','ocupacion','empresa','motivo_viaje','nacionalidad','procedencia')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

class  RegistrosTable2(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = RegistroHotel
        fields = ('destino','placa_vehiculo','dias_estadia','no_adultos','no_niños','equipaje','pagado','no_recibo_caja')
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

    Detalle = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnSelDet" type="button" class="btn btn-warning btn-sm" type="submit" href="{% url "detalle_pedidos_pendientes_habitacion_list" id=record.id %}" value="seleccionar" ><i <span class="material-icons">menu</span</i></a>'''
    )

class PedidosCajaDetalleTable(tables.Table):
    valor = ColumnWithThousandsSeparator()
    valor_total = ColumnWithThousandsSeparator()
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = PedidoCajaDetalle
        fields = ("numero","IdItem","valor","cantidad","valor_total" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}            


class RecibosCajaTableHotel(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor = ColumnWithThousandsSeparator()
    class Meta:
        model = ReciboCaja
        fields = ("numero","fecha","detalle","IdTercero","IdMesa","IdHabitacion","IdCaja","pedido_caja","valor","pagado","IdUsuario" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

    Pago = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnPagar" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_pago_estadia" id=record.id %}" value="seleccionar" ><i <span class="material-icons">add</span</i></a>'''
     )
    PDF = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnImpresionReciboCaja" type="button" class="btn btn-primary" type="submit" href="{% url "impresion_recibo_caja_hotel" id=record.id %}" value="seleccionar" ><i <span class="material-icons">print</span</i></a>'''
     )
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraReciboCaja" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrado_recibo_caja_hotel" id=record.id %}" value="editar" ><i <span class="material-icons">delete</span</i></a>'''
     )

    
class RecibosCajaDetalleTableHotel(tables.Table):
    valor = ColumnWithThousandsSeparator()
    valor_total = ColumnWithThousandsSeparator()
    class Meta:
        model = ReciboCajaDetalle
        fields = ("numero","pedido_caja","valor","IdItem","cantidad","valor_total")
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}

class PagosCajaHotelTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    valor = ColumnWithThousandsSeparator()
    class Meta:
        model = PagoReciboCaja
        fields = ("numero","fecha","detalle","IdCaja","IdTercero","recibo_caja","IdTipoPago","IdTarjetaCredito","valor","IdUsuario" )
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}
    
    PDF = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnImpresionPagoCaja" type="button" class="btn btn-primary" type="submit" href="{% url "impresion_pago_recibo_caja_hotel" id=record.id %}" value="seleccionar" ><i <span class="material-icons">print</span</i></a>'''
    )
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraPago" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "valida_borrado_pago_recibo_caja_hotel" id=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
    )        

class  AcompañanteHotelTable(tables.Table):
    id = tables.Column(
        attrs={"td": {"id": "id"}})
    class Meta:
        model = AcompañanteHotel
        fields = ('IdRegistro','identificacion','IdTipoIdentiicacion','identifica_de','apenom','lugar_residencia')
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {"class": "table table-hover table-sm"}
              
    Editar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnEditaReserva" type="button" class="btn btn-success btn-sm" type="submit" href="{% url "edita_acompañante_hotel" pk=record.id %}" value="editar" ><i <span class="material-icons">edit</span</i></a>'''
     )    
    Borrar = tables.TemplateColumn(
        '{% csrf_token %}'
        '''<a id="btnBorraReserva" type="button" class="btn btn-danger btn-sm" type="submit" href="{% url "borra_acompañante_hotel" pk=record.id %}" value="borrar" ><i <span class="material-icons">delete</span</i></a>'''
     )
