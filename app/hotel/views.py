from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from datetime import timedelta,date
from django_tables2.views import SingleTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest,HttpResponse, HttpRequest, JsonResponse,HttpResponseRedirect
from django.core import serializers
from django.core.serializers import serialize
from django.db.models import Q,Sum
from django.utils import timezone

from core.forms import TerceroForm
from core.models import Tercero,TipoIdentificacion
from core.tables import TercerosRegistroTable
from core.filters import TerceroNombreFilter
from .models import TipoHabitacion,Habitacion,ReservaHabitacion,RegistroHotel,AcompañanteHotel
from .forms import TipoHabitacionForm,HabitacionForm,ReservaForm,ValidaReservaForm,RegistroForm,TerceroRegistroHotelForm,CheckOutForm,LiquidaEstadiaForm,AcompañanteHotelForm
from .tables import TipoHabitacionTable,Habitaciones1Table,ReservasTable,ReservasTable1,RegistrosTable,RegistrosTable1,RegistrosTable2,PedidosCajaTable,PedidosCajaDetalleTable,RecibosCajaTableHotel,RecibosCajaDetalleTableHotel,PagosCajaHotelTable,AcompañanteHotelTable
from .filters import ReservasFilter,RegistrosFilter 
from caja.forms import PagoReciboCaja,PagoReciboCajaForm
from caja.models import ReciboCaja,TipoDocumentoCaja,PedidoCaja,ReciboCajaDetalle,PedidoCajaDetalle,Caja,TipoIngresoCaja
from caja.tables import PedidosCajaTableConsolidado 
from core.models import ValorDefecto,Sucursal
from inventarios.models import MaestroItem
from restaurante.models import Mesa

from datetime import datetime
import json
from django.forms import formset_factory 

import io
from io import BytesIO
from io import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
import xlsxwriter
from django.http import FileResponse
import csv

from core.models import Empresa

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from  reportlab.lib.styles import ParagraphStyle


# Create your views here.
def TiposHabitacionListView(request):
    queryset = TipoHabitacion.objects.all()
    tipo_habitacion = TipoHabitacionTable(queryset)
    tipo_habitacion.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'tipo_habitacion':tipo_habitacion}
    return render(request, 'hotel/tipo_habitacion_lista.html', context) 

class CreaTiposHabitacionView(LoginRequiredMixin,CreateView):
    model = TipoHabitacion
    template_name = 'hotel/tipo_habitacion_form.html'
    form_class = TipoHabitacionForm
    
    def get_success_url(self):
        return reverse_lazy('tipos_habitacion_list')
       
class EditaTipoHabitacionView(LoginRequiredMixin,UpdateView):
    model = TipoHabitacion
    fields = ['idTipoHabitacion','descripcion']
    template_name = 'hotel/tipo_habitacion_form.html'
    success_url = reverse_lazy('tipos_habitacion_list')

class BorraTipoHabitacionView(LoginRequiredMixin,DeleteView):
    model = TipoHabitacion
    success_url = reverse_lazy('tipos_habitacion_list')
    template_name = 'hotel/confirma_borrado.html'


def HabitacionesListView(request):
    queryset = Habitacion.objects.all()
    habitacion = Habitaciones1Table(queryset)
    habitacion.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'habitacion':habitacion}
    return render(request, 'hotel/habitacion_lista.html', context) 

class CreaHabitacionView(LoginRequiredMixin,CreateView):
    model = Habitacion
    template_name = 'hotel/habitacion_form.html'
    form_class = HabitacionForm
    
    def get_success_url(self):
        return reverse_lazy('habitacion_list')
       
class EditaHabitacionView(LoginRequiredMixin,UpdateView):
    model = Habitacion
    fields = ['idHabitacion','IdTipoHabitacion','descripcion','valor_noche','ocupada']
    template_name = 'hotel/habitacion_form.html'
    success_url = reverse_lazy('habitaciones_list')

class BorraHabitacionView(LoginRequiredMixin,DeleteView):
    model = Habitacion
    success_url = reverse_lazy('habitaciones_list')
    template_name = 'hotel/confirma_borrado.html'

def ReservasListView(request):
    #queryset = ReservaHabitacion.objects.filter(fecha_salida__gte=datetime.now()).order_by('-fecha_reserva')
    queryset = ReservaHabitacion.objects.all().order_by('-fecha_reserva')
    f = ReservasFilter(request.GET,queryset=queryset)
    reserva_habitacion = ReservasTable(f.qs)
    request.session['lista_id_filtro_reservas_hotel'] = False
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
        request.session['lista_id_filtro_reservas_hotel']  = lista_id
    reserva_habitacion.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'reserva_habitacion':reserva_habitacion,'filter':f}
    return render(request, 'hotel/reserva_lista.html', context) 

def ReservasDetalleListView(request,id):
    queryset = ReservaHabitacion.objects.filter(id=id)
    reserva_habitacion_detalle = ReservasTable1(queryset)
    reserva_habitacion_detalle.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'reserva_habitacion_detalle':reserva_habitacion_detalle}
    return render(request, 'hotel/reserva_detalle_lista.html', context) 

def AjaxHabitaciones(request):
    habitaciones = Habitacion.objects.all().values('descripcion', 'id')
    return HttpResponse( json.dumps( list(habitaciones)), content_type='application/json' )

def GuardaFechaInicialReserva(request):
    fecha_inicial_reserva = request.GET.get('fecha_inicial', None)
    request.session['fecha_inicial_reserva'] = fecha_inicial_reserva 
    data={'a':0}
    return JsonResponse(data)

def GuardaFechaFinalReserva(request):
    fecha_final_reserva = request.GET.get('fecha_final', None)
    request.session['fecha_final_reserva'] = fecha_final_reserva 
    data={'a':0}
    return JsonResponse(data)

def GuardaHabitacionReserva(request):
    idhabitacion_reserva = request.GET.get('id', None)
    request.session['id_habitacion_reserva'] = idhabitacion_reserva 
    data={'a':0}
    return JsonResponse(data)

from random import *

def ValidaReservaView(request):
    if request.POST:
        form = ValidaReservaForm(request.POST, request.FILES)
        return HttpResponseRedirect('reservas_list')
    else:
        form = ValidaReservaForm(request.POST, request.FILES)
        context = {'form':form}
        return render(request, 'hotel/valida_fechas_reserva.html', context)
    
def ValidaFechasReservaView(request):
    fecha_inicial = request.session['fecha_inicial_reserva']
    fecha_final = request.session['fecha_final_reserva']
    idhabitacion = request.session['id_habitacion_reserva']
    existe_reserva = valida_fechas_reserva(fecha_inicial,fecha_final,idhabitacion)
    if existe_reserva == False:    
        return redirect('crea_reserva')    
    else:
        mensaje1 = "Ya existe una reserva en esa fecha "
        mensaje2 = ""
        mensaje3 = ""
        parametro = 1  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'hotel/mensaje_error_reserva.html', context)

def valida_fechas_reserva(fecha_inicial,fech_final,idhabitacion):
    sw = False
    #if ReservaHabitacion.objects.filter(Q(id=idhabitacion) & Q(fecha_ingreso__gte=fecha_inicial)).exists():
    #reservas = ReservaHabitacion.objects.filter(Q(id=idhabitacion) & Q(fecha_ingreso__gte=fecha_inicial))
    reservas = ReservaHabitacion.objects.filter(IdHabitacion_id=idhabitacion)
    fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
    for res in reservas:
        fecha_salida = res.fecha_salida - timedelta(days=1)
        if fecha_inicial >= res.fecha_ingreso and fecha_inicial <= fecha_salida :
            #and fecha_inicial <= res.fecha_salida :
            sw = True
    return(sw)            

class CreaReservaView(LoginRequiredMixin,CreateView):
    model = ReservaHabitacion
    template_name = 'hotel/reserva_form.html'
    form_class = ReservaForm
    
    def get_initial(self,*args,**kwargs):
        initial=super(CreaReservaView,self).get_initial(**kwargs)
        fecha_inicial = self.request.session['fecha_inicial_reserva']
        fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d')
        fecha_final = self.request.session['fecha_final_reserva']
        fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d')
        initial['IdHabitacion'] = self.request.session['id_habitacion_reserva']
        return initial
    
    def get_success_url(self):
        return reverse_lazy('reservas_list')

    def form_valid(self, form):
        if form.is_valid():
            fecha_inicial = self.request.session['fecha_inicial_reserva']
            fecha_inicial = datetime.strptime(fecha_inicial, '%Y-%m-%d')
            fecha_final = self.request.session['fecha_final_reserva']
            fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d')
            reserva = form.save(commit=False)
            reserva.fecha_ingreso = fecha_inicial
            reserva.fecha_salida = fecha_final
            reserva.IdUsuario_id = self.request.user.id
            reserva.pin = int(1000000*random())
            registros = ReservaHabitacion.objects.all()
            num_res = 0
            for reg in registros:
                num_res += 1
            reserva.fecha_reserva = date.today().strftime('%Y-%m-%d')
            lconsecutivo = str(num_res+1).zfill(15)
            reserva.consecutivo = lconsecutivo
            reserva.save()
            reserva = ReservaHabitacion.objects.get(consecutivo=lconsecutivo)
            noches = (reserva.fecha_salida-reserva.fecha_ingreso).days
            ReservaHabitacion.objects.filter(consecutivo=lconsecutivo).update(no_de_noches = noches)
            return redirect('reservas_list')  

class EditaReservaView(LoginRequiredMixin,UpdateView):
    model = ReservaHabitacion
    fields = ['descripcion','valor_reserva','nombre_reserva','telefono','email']
    template_name = 'hotel/reserva_edit_form.html'
    success_url = reverse_lazy('reservas_list')

class BorraReservaView(LoginRequiredMixin,DeleteView):
    model = ReservaHabitacion
    success_url = reverse_lazy('reservas_list')
    template_name = 'hotel/confirma_borrado.html'

class BuscaTerceroRegistroView(SingleTableMixin, FilterView):
    table_class = TercerosRegistroTable
    model = Tercero
    template_name = "core/terceros_registro_filter.html"
    filterset_class = TerceroNombreFilter
    paginate_by = 8

def SeleccionaTerceroRegistroHotelView(request):
    idTercero = request.GET.get('id', None)
    request.session['idtercero'] = idTercero
    data = {'id':idTercero}
    return JsonResponse(data) 

class CreaTerceroRegistroHotelView(LoginRequiredMixin,CreateView):
    model = Tercero
    template_name = 'hotel/tercero_registro_hotel_form.html'
    form_class = TerceroRegistroHotelForm
    
    def get_success_url(self):
        idtercero = self.object.id
        self.request.session['idtercero' ] = idtercero
        return redirect('crea_registro')   

    def form_valid(self, form):
        if form.is_valid():
            tercero = form.save(commit=False)
            registros = Tercero.objects.count()
            sregistro= str(registros+1)
            consec = sregistro.zfill(8)
            tercero.IdUsuario_id = self.request.user.id
            tercero.save()
            self.request.session['idtercero'] = tercero.id
            Tercero.objects.filter(id=tercero.id).update(apenom = tercero.apel1.strip()+" "+tercero.apel2.strip()+" "+tercero.nombre1.strip()+" "+tercero.nombre2.strip())
            return redirect('crea_registro')

def AjaxValidarHabitacion(request):
    idhabitacion = request.GET.get('id', None)
    print('IdHabitacion:',idhabitacion)
    habitacion = Habitacion.objects.get(id=idhabitacion)
    print('Habitacion',habitacion.ocupada)
    if habitacion.ocupada == True: 
        data = {'ocupada': 1}
    else:
        data = {'ocupada': 0}    
    print('Data ',data)
    return JsonResponse(data)

def GuardaIdRegistro(request):
    idregistro = request.GET.get('id', None)
    request.session['idregistro'] = idregistro
    registro = RegistroHotel.objects.get(id=idregistro)
    request.session['idhabitacion'] = registro.IdHabitacion_id
    print('Registro: ',id)
    print('Habitacion: ',registro.IdHabitacion_id)
    data={'a':0}
    return JsonResponse(data)
            
class CreaRegistroView(LoginRequiredMixin,CreateView): 
    model = RegistroHotel
    template_name = 'hotel/registro_form.html'
    form_class = RegistroForm
    
    def get_success_url(self):
        idregistro = self.object.id
        self.request.session['idregistro' ] = idregistro
        return redirect('registros_list')   

    def form_valid(self, form):
        if form.is_valid():
            registro_hotel = form.save(commit=False)
            registros = RegistroHotel.objects.count()
            sregistro= str(registros+1)
            consec = sregistro.zfill(8)
            registro_hotel.consecutivo = consec
            registro_hotel.IdUsuario_id = self.request.user.id
            registro_hotel.IdTercero_id = self.request.session['idtercero']
            registro_hotel.check_out = None
            registro_hotel.hora_check_out = None
            registro_hotel.save()
            self.request.session['idregistro'] = registro_hotel.id
            #RegistroHotel.objects.filter(id=registro_hotel.id).update(hora_check_out=None)
            Habitacion.objects.filter(id=registro_hotel.IdHabitacion_id).update(ocupada=True)
            return redirect('registros_list')
   
def RegistrosListView(request):
    queryset = RegistroHotel.objects.all().order_by('-consecutivo')
    f = RegistrosFilter(request.GET,queryset=queryset)
    registros = RegistrosTable(f.qs)
    request.session['lista_id_filtro_registros_hotel'] = False
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
        request.session['lista_id_filtro_registros_hotel']  = lista_id
    registros.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'registros':registros,'filter':f}
    return render(request, 'hotel/registro_lista.html', context) 

def RegistroDetalleListView(request,id):
    queryset = RegistroHotel.objects.filter(id=id).order_by('-check_in')
    f = RegistrosFilter(request.GET,queryset=queryset)
    registro = RegistrosTable(f.qs)
    registro1 = RegistrosTable1(f.qs)
    registro2 = RegistrosTable2(f.qs)
    #registro.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'registro':registro,'registro1':registro1,'registro2':registro2,'filter':f}
    return render(request, 'hotel/registro_detalle_lista.html', context)

class EditaRegistroView(LoginRequiredMixin,UpdateView):
    model = RegistroHotel
    fields = ['IdHabitacion','IdTercero','descripcion','tarifa_habitacion','check_in',
                  'ocupacion','empresa','motivo_viaje','procedencia','destino','nacionalidad','placa_vehiculo','dias_estadia','no_adultos','no_ninos','equipaje']
    template_name = 'hotel/registro_edit_form.html'
        
    def get_success_url(self):
        idregistro = self.request.session['idregistro']
        return reverse_lazy('registro_detalle_list',kwargs={'id': idregistro})  
    

class BorraRegistroView(LoginRequiredMixin,DeleteView):
    model = RegistroHotel
    success_url = reverse_lazy('registros_list')
    template_name = 'hotel/confirma_borrado.html'

def RegistroPedidosCajaConsolidadosView(request,id):
    request.session['pedidosconsolidados'] = True
    consolidar = request.session['consolidar'] = True
    registro = RegistroHotel.objects.get(id=id)
    pedidos = PedidoCaja.objects.filter(IdHabitacion_id=registro.IdHabitacion_id, cerrado=False)
    idpedidos_cons=[]
    for i in pedidos:
        idpedidos_cons.append(i.id)
        request.session['idhabitacion'] = i.IdHabitacion_id
        request.session['idpedidocaja'] = i.id
    numeros_pedidos = pedidos.values_list('numero', flat=True)
    detalle = PedidoCajaDetalle.objects.filter(numero__in=numeros_pedidos)
    total_pedidos = PedidoCaja.objects.filter(IdHabitacion_id=registro.IdHabitacion_id,cerrado=False).aggregate(Sum('valor_total'))['valor_total__sum']     
    idregistro = request.session['idregistro']
    context = {'pedidos':pedidos,'detalle':detalle,'total_pedidos':total_pedidos,'idregistro':idregistro}
    return render(request, 'hotel/hotel_pedidos_caja_lista_consolidado.html', context)
    
""" def ImpresionPedidosCajaRegistro(request):
    id = request.session['idregistro']
    registro = RegistroHotel.objects.get(id=id)
    consolidar = request.session['consolidar']
    request.session['id_habitacion_consolidar'] = registro.IdHabitacion_id
    return redirect('impresion_pedidos_caja_pdf') """

def ImpresionPedidosCajaRegistroXlsView(request):
    id = request.session['idregistro']
    registro = RegistroHotel.objects.get(id=id)
    idhabitacion = registro.IdHabitacion_id
    request.session['id_habitacion_consolidar'] = registro.IdHabitacion_id
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1','Numero' )
    worksheet.write('B1','Fecha' )
    worksheet.write('C1','Caja')
    worksheet.write('D1','Mesa')
    worksheet.write('E1','Habitación')
    worksheet.write('F1','Recibo Caja')
    worksheet.write('G1','Valor')
    worksheet.write('H1','Usuario')
    idcaja = request.session['idcaja']
    pedidos = PedidoCaja.objects.filter(IdHabitacion_id=idhabitacion,cerrado=False).order_by('-numero')
    registros = PedidoCaja.objects.filter(IdHabitacion_id=idhabitacion,cerrado=False).count()
    numeros_pedidos = pedidos.values_list('numero', flat=True)
    pedido_detalles = PedidoCajaDetalle.objects.filter(numero__in=numeros_pedidos)
    habitacion = Habitacion.objects.get(id=registro.IdHabitacion_id )
    total_pedido = pedido_detalles.aggregate(Sum('valor_total'))['valor_total__sum']
    n=2
    sw = 0
    tw= 0
    for j in pedidos:     
        nn = str(n)
        numero = j.numero
        fecha = j.fecha.strftime("%d/%m/%Y")
        caja = j.IdCaja
        mesa = j.IdMesa
        habitacion = j.IdHabitacion
        valor_total = j.valor_total
        recibo_caja = j.recibo_caja
        usuario = j.IdUsuario
        if sw == 0:
            exec("worksheet.write('A"+nn+"','"+numero+"' )")
            exec("worksheet.write('B"+nn+"','"+str(fecha)+"' )")
            exec("worksheet.write('C"+nn+"','"+str(caja)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(mesa)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(habitacion)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(recibo_caja)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(valor_total)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(usuario)+"' )")
        pedido_detalle = PedidoCajaDetalle.objects.filter(numero=j.numero)
        n +=1
        mm = str(n)
        if tw == 0:
            exec("worksheet.write('A"+mm+"','Número' )")
            exec("worksheet.write('B"+mm+"','Producto' )")
            exec("worksheet.write('C"+mm+"','Cantidad' )")
            exec("worksheet.write('D"+mm+"','Valor' )")
            exec("worksheet.write('E"+mm+"','Valor Total' )")
            exec("worksheet.write('F"+mm+"','Fecha' )")
            n +=1
        for i in pedido_detalle:
            mm = str(n)
            producto = i.IdItem
            cantidad = i.cantidad
            valor = i. valor
            valor_total = i.valor_total
            fecha = j.created.strftime("%Y-%m-%d %H:%M:%S")
            exec("worksheet.write('A"+mm+"','"+numero+"' )")
            exec("worksheet.write('B"+mm+"','"+str(producto)+"' )")
            exec("worksheet.write('C"+mm+"','"+str(cantidad)+"' )")
            exec("worksheet.write('D"+mm+"','"+str(valor)+"' )")
            exec("worksheet.write('E"+mm+"','"+str(valor_total)+"' )")
            exec("worksheet.write('F"+mm+"','"+str(fecha)+"' )") 
            n += 1
            tw=1
    n += 1
    workbook.close()
    output.seek(0)
    filename = 'pedidos_caja.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    

def ImpresionPedidosCajaRegistroView(request):
    id = request.session['idregistro']
    registro = RegistroHotel.objects.get(id=id)
    idhabitacion = registro.IdHabitacion_id
    y = 0
    response = HttpResponse(content_type='application/pdf')
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    response = HttpResponse(content_type='application/pdf')
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    archivo_imagen = settings.MEDIA_ROOT+'/img/logo_empresa.png'
    pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)
    pdf.setFont("Helvetica", 16)
    y = 770
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(170, y, u""+empresa.nombre)
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(200, y, u"PEDIDOS")
    pdf.setFont("Helvetica", 9)
    y -= 20
    x = 380
    pdf.line(30,y,x,y)
    y -= 10
    pdf.drawString(180,y , u"Fecha : "+timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    y -= 10
    pdf.line(30,y,x,y)
    y -= 10
    habitacion = Habitacion.objects.get(id=idhabitacion )
    pdf.drawString(110, y, u"Habitación   : "+str(habitacion.descripcion))
    
    pedidos = PedidoCaja.objects.filter(IdHabitacion_id=idhabitacion,cerrado=False).order_by('-numero')
    numeros_pedidos = pedidos.values_list('numero', flat=True)
    pedido_detalles = PedidoCajaDetalle.objects.filter(numero__in=numeros_pedidos)
    registros = PedidoCajaDetalle.objects.filter(numero__in=numeros_pedidos).count()
    print('Registros : ',registros)
    y -= 0
    y = y -(registros*25)
    if y<=40:
        pdf.showPage()
        y= 750    
    if  pedido_detalles:
        total_recibo = pedido_detalles.aggregate(Sum('valor_total'))['valor_total__sum']
        total = total_recibo
        encabezados = ('RecCaja','Producto', 'Cantidad', 'Valor Unit.', 'Valor Total','Fecha/Hora')
        detalles = [(cuerpo.numero,cuerpo.IdItem.descripcion[0:30], cuerpo.cantidad, '{:,}'.format(cuerpo.valor), '{:,}'.format(cuerpo.valor_total),cuerpo.created.strftime("%Y-%m-%d %H:%M:%S")) for cuerpo in pedido_detalles]
        detalle_recibo = Table([encabezados] + detalles, colWidths=[1.5 * cm,4 * cm, 1.5 * cm, 2 * cm, 2.6 * cm])
        detalle_recibo.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1), 7),
        ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_recibo.wrapOn(pdf, 300, 800)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_recibo.drawOn(pdf, 30,y)
        y -= 20
        pdf.setFont("Helvetica", 9)
        if total_recibo:
            pdf.drawString(240, y, u"Total Recibo      : "+('{:,}'.format(total_recibo)+'.00'))
          
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

class CheckOutView(LoginRequiredMixin,UpdateView):
    model = RegistroHotel
    #fields = ['check_out','descripcion']
    template_name = 'hotel/check_out_form.html'
    form_class = CheckOutForm
    #success_url = reverse_lazy('registros_list') 

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            pk =self.kwargs.get("pk")
            registro = RegistroHotel.objects.get(id=pk)
            self.request.session['idregistro'] = registro.id
            noches = (registro.check_out-registro.check_in).days
            RegistroHotel.objects.filter(id=pk).update(hora_check_out = datetime.now(),no_de_noches = noches)
            Habitacion.objects.filter(id=registro.IdHabitacion_id).update(ocupada=False)
            idregistro = self.request.session['idregistro']
        return redirect('registro_detalle_list',idregistro)
        
             
def ValidaPagoEstadiaView(request,id):
    recibo_caja = ReciboCaja.objects.get(id=id) 
    registro = RegistroHotel.objects.get(consecutivo=recibo_caja.registro)
    if registro.pagado == False :
        print('aqui............')
        return redirect('pago_estadia')
    else:
        if PagoReciboCaja.objects.filter(numero=registro.no_recibo_caja).exists():
            pago_recibo_caja = PagoReciboCaja.objects.get(numero=registro.no_recibo_caja)
            mensaje1="Pago ya efectuado, Recibo de Caja No. :"+pago_recibo_caja.numero+chr(32)
            mensaje2 = ''
            mensaje3 = ''
            return render(request,'hotel/mensaje_error_pago_estadia.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3})        
        else:
            if recibo_caja.valor == 0:
                mensaje1="Recibo de caja con valor = 0,"
                mensaje2 = '<Puede estar anulado>'
                mensaje3 = ''    
                return render(request,'hotel/mensaje_error_pago_estadia.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3})
            else:
                return redirect('recibo_caja_hotel') 



def SeleccionaCajaReciboCajaEstadiaView(request):
    #request.session['idregistro'] = id
    #registro = RegistroHotel.objects.get(id=id)
    #request.session['idhabitacion'] = registro.IdHabitacion_id
    context = {'x':0}
    return render(request, 'hotel/selecciona_caja_recibo_caja_estadia.html', context) 

def PedidosPendientesHabitacionListView(request,id):
    request.session['idregistro'] = id
    registro = RegistroHotel.objects.get(id=id)
    idhabitacion = registro.IdHabitacion_id
    request.session['idhabitacion'] = idhabitacion
    queryset = PedidoCaja.objects.filter(IdHabitacion_id=idhabitacion,cerrado=0).order_by('numero').reverse()
    total_pedidos = PedidoCaja.objects.filter(IdHabitacion_id=idhabitacion,cerrado=0).aggregate(Sum('valor_total'))['valor_total__sum']     
    pedidos_caja = PedidosCajaTable(queryset)
    pedidos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
    context = {'pedidos_caja':pedidos_caja,'total_pedidos':total_pedidos}
    return render(request, 'hotel/pedidos_caja_lista_habitacion.html', context) 

def DetallePedidosPendientesHabitacionListView(request,id):
    idregistro = request.session['idregistro']
    idhabitacion = request.session['idhabitacion']
    pedido = PedidoCaja.objects.get(id=id)
    queryset = PedidoCajaDetalle.objects.filter(numero=pedido.numero).order_by('numero').reverse()
    total_pedidos = PedidoCajaDetalle.objects.filter(numero=pedido.numero).aggregate(Sum('valor_total'))['valor_total__sum']     
    pedido_caja = PedidosCajaDetalleTable(queryset)
    pedido_caja.paginate(page=request.GET.get("page", 1), per_page=8)
    context = {'pedido_caja':pedido_caja,'total_pedidos':total_pedidos,'idhabitacion':idhabitacion,'idregistro':idregistro}
    return render(request, 'hotel/pedidos_detalle_caja_lista_habitacion.html', context) 

class LiquidaEstadiaView(LoginRequiredMixin,UpdateView):
    model = RegistroHotel
    template_name = 'hotel/liquida_estadia_form.html'
    form_class = LiquidaEstadiaForm
    
    def get_initial(self,*args,**kwargs):
        idregistro = self.request.session['idregistro']
        registro = RegistroHotel.objects.get(id=idregistro)
        initial=super(LiquidaEstadiaView,self).get_initial(**kwargs)
        initial['IdHabitacion'] = self.request.session['idhabitacion']
        initial['check_in'] = registro.check_in
        #initial['hora_check_in'] = registro.hora_check_in
        initial['check_out'] = registro.check_out
        #initial['hora_check_out'] = registro.hora_check_out
        initial['no_de_dias'] = registro.no_de_dias
        initial['no_de_noches'] = registro.no_de_noches  
        return initial
    
    def get_success_url(self):
        idregistro = self.request.session['idregistro']
        return reverse_lazy('registro_detalle_list',kwargs={'id': idregistro})   

def ValidaCreacionReciboCajaEstadiaView(request):
    idregistro = request.session['idregistro']
    #idregistro = id
    registro = RegistroHotel.objects.get(id=idregistro)
    if ReciboCaja.objects.filter(registro=registro.consecutivo).exists():
        recibo_caja = ReciboCaja.objects.filter(registro=registro.consecutivo)
        n = 0
        for j in recibo_caja:
            if j.valor > 0:
                n  += 1
                return redirect('recibo_caja_hotel')
        if n == 0:    
            return redirect('selecciona_caja_recibo_caja_estadia')          
    else:
        return redirect('selecciona_caja_recibo_caja_estadia')      
    

def ReciboCajaHotelView(request):
    idregistro = request.session['idregistro']
    registro = RegistroHotel.objects.get(id=idregistro)
    recibo = ReciboCaja.objects.get(registro=registro.consecutivo,valor__gt=0)
    caja = Caja.objects.get(id=recibo.IdCaja_id)    
    queryset = ReciboCaja.objects.filter(registro=registro.consecutivo,valor__gt=0)
    recibo_caja = RecibosCajaTableHotel(queryset)
    total_recibos =ReciboCaja.objects.filter(registro=registro.consecutivo).aggregate(Sum('valor'))['valor__sum']
    queryset1 = ReciboCajaDetalle.objects.filter(numero=recibo.numero)
    recibo_caja_detalle = RecibosCajaDetalleTableHotel(queryset1)
    recibo_caja_detalle.paginate(page=request.GET.get("page", 1), per_page=8)
    idregistro = request.session['idregistro']
    context = {'recibo_caja':recibo_caja,'recibo_caja_detalle':recibo_caja_detalle,'nombre_caja':caja.descripcion,'total_recibos':total_recibos,'idregistro':idregistro}
    return render(request, 'hotel/recibos_caja_hotel_lista.html', context)

def ReciboCajaDetalleHotelView(request,id):
    idregistro = request.session['idregistro']
    registro = RegistroHotel.objects.get(id=idregistro)
    recibo = ReciboCaja.objects.get(registro=registro.consecutivo)
    caja = Caja.objects.get(id=recibo.IdCaja_id)
    queryset = ReciboCaja.objects.filter(id=recibo.id)
    recibo_caja = RecibosCajaTableHotel(queryset)

    queryset1 = ReciboCajaDetalle.objects.filter(IdReciboCaja_id=recibo.id)
    recibo_detalle_caja = RecibosCajaDetalleTableHotel(queryset1)
    total_recibos =ReciboCajaDetalle.objects.filter(IdReciboCaja_id=recibo.id).aggregate(Sum('valor_total'))['valor_total__sum']
    recibo_detalle_caja.paginate(page=request.GET.get("page", 1), per_page=8)
    context = {'recibo_caja':recibo_caja,'recibo_detalle_caja':recibo_detalle_caja,'nombre_caja':caja.descripcion,'total_recibos':total_recibos}
    return render(request, 'hotel/recibos_caja_hotel_detalle.html', context)

def BuscaPagoHotelView(request):
    idrecibocaja  = request.session['idrecibocaja']
    recibo_caja = ReciboCaja.objects.get(id=idrecibocaja)
    pago = PagoReciboCaja.objects.get(recibo_caja=recibo_caja.numero,estado=1)
    idcaja = pago.IdCaja
    nombre_caja = idcaja.descripcion
    pagos_caja = PagosCajaHotelTable(PagoReciboCaja.objects.filter(recibo_caja=recibo_caja.numero,estado=True))
    total_pagos =PagoReciboCaja.objects.filter(recibo_caja=recibo_caja.numero).aggregate(Sum('valor'))['valor__sum']
    context = {'pagos_caja':pagos_caja,'total_pagos': total_pagos,'nombre_caja':nombre_caja}
    return render(request, 'hotel/pagos_caja_hotel_lista.html', context) 

def ValidaBorradoPagoReciboCajaHotelView(request,id):
    request.session['idpago'] = id
    mensaje1="Esta seguro de borrar este pago?"
    mensaje2 = ''
    mensaje3 = ''
    return render(request,'hotel/mensaje_confirma_borra_pago_caja_hotel.html',{'mensaje1':mensaje1})

def BorraPagoReciboCajaHotelView(request,id):
    if id == 1:
        idpago = request.session['idpago']
        pago = PagoReciboCaja.objects.get(id=idpago)
        ReciboCaja.objects.filter(numero=pago.recibo_caja).update(pagado=False,pedido_caja='')
        valor_defecto = ValorDefecto.objects.get(idValor='07')
        if valor_defecto.valor == 1:
            PagoReciboCaja.objects.filter(id=idpago).delete()
        else:
            #valor_defecto = ValorDefecto.objects.get(idValor='08')
            #tercero = Tercero.objects.get(identificacion=valor_defecto.valor)
            PagoReciboCaja.objects.filter(id=idpago).update(detalle='Pago Anulado',valor=0,IdTipoPago_id=1,IdCaja_id=1,IdTarjetaCredito_id=1,recibo_caja='',estado=0)
    else:
        idpago = request.session['idpago']
        pago = PagoReciboCaja.objects.get(id=idpago)
        idcaja = pago.IdCaja_id
        request.session['idcaja'] = idcaja
    return redirect('recibo_caja_hotel')
                
def CreaReciboCajaEstadiaView(request,id):
    idcaja = id
    request.session['idcaja'] = idcaja
    #registro = RegistroHotel.objects.get(id=id)
    idregistro = request.session['idregistro']
    registro = RegistroHotel.objects.get(id=idregistro)
    idtercero = registro.IdTercero_id
    idhabitacion = registro.IdHabitacion_id
    mesa = Mesa.objects.get(idMesa='*')
    sucursal_defecto = ValorDefecto.objects.get(idValor='01')
    sucursal =Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
    recibo_caja = ReciboCaja()
    tipodocumento = TipoDocumentoCaja.objects.get(idTipo='02')
    anumero = tipodocumento.actual +1
    cnumero = str(anumero).zfill(tipodocumento.longitud)
    cnumero = tipodocumento.caracteres+cnumero
    recibo_caja.IdTipoDocumento_id = tipodocumento.id 
    recibo_caja.numero =  cnumero
    recibo_caja.fecha = date.today()
    recibo_caja.estado = True
    recibo_caja.pedido_caja = 'Varios'
    recibo_caja.IdTercero_id = idtercero
    recibo_caja.IdMesa_id = mesa.id
    recibo_caja.IdHabitacion_id = idhabitacion
    recibo_caja.IdCaja_id = idcaja
    recibo_caja.IdSucursal_id = sucursal_defecto.id
    recibo_caja.IdUsuario_id = request.user.id
    recibo_caja.registro = registro.consecutivo
    recibo_caja.save()
    pedidos = PedidoCaja.objects.filter(IdHabitacion_id=idhabitacion,cerrado=False)
    for n in pedidos:
        PedidoCaja.objects.filter(numero=n.numero).update(cerrado=True,recibo_caja=cnumero)
    TipoDocumentoCaja.objects.filter(idTipo='02').update(actual = anumero ) 
    recibo_caja = ReciboCaja.objects.get(numero=cnumero)
    recibo_caja_detalle = ReciboCajaDetalle()
    tot_val_rec = 0
    #valor_defecto = ValorDefecto.objects.get(idValor=10)
    cantidad_estadia= MaestroItem.objects.filter(estadia=True).count()
    if cantidad_estadia == 1:
        item = MaestroItem.objects.get(estadia=True)
        #for n in idpedidos_cons:
        if pedidos:
            for n in pedidos:
                pedido_caja = PedidoCaja.objects.get(numero=n.numero)
                pedido_caja_detalle = PedidoCajaDetalle.objects.filter(numero=pedido_caja.numero)
                for ped in pedido_caja_detalle:
                    recibo_caja_detalle.numero = cnumero
                    recibo_caja_detalle.IdTipoDocumento_id = tipodocumento.id 
                    recibo_caja_detalle.IdReciboCaja_id = recibo_caja.id
                    recibo_caja_detalle.IdPedidoCajaDetalle_id = ped.id
                    recibo_caja_detalle.pedido_caja = ped.numero
                    recibo_caja_detalle.IdItem_id = ped.IdItem_id
                    recibo_caja_detalle.valor = ped.valor
                    recibo_caja_detalle.cantidad = ped.cantidad
                    recibo_caja_detalle.valor_total = ped.valor_total
                    tot_val_rec = tot_val_rec + ped.valor_total
                    recibo_caja_detalle.save()
                    recibo_caja_detalle.id += 1
            recibo_caja_detalle.numero = cnumero
            recibo_caja_detalle.IdTipoDocumento_id = tipodocumento.id 
            recibo_caja_detalle.IdReciboCaja_id = recibo_caja.id
            recibo_caja_detalle.IdPedidoCajaDetalle_id = ped.id
            recibo_caja_detalle.pedido_caja = ped.numero
            recibo_caja_detalle.IdItem_id = item.id
            recibo_caja_detalle.valor = registro.valor_pago
            recibo_caja_detalle.cantidad = 1
            recibo_caja_detalle.valor_total = registro.valor_pago
            tot_val_rec = tot_val_rec + registro.valor_pago
            recibo_caja_detalle.save()
            recibo_caja_detalle.id += 1
            RegistroHotel.objects.filter(id=idregistro).update(no_recibo_caja=cnumero,pagado=True) 
            ReciboCaja.objects.filter(numero=cnumero).update(valor=tot_val_rec) 
        else:
            iduser = request.user.id
            tipodocumento = TipoDocumentoCaja.objects.get(idTipo='01')
            anumero = tipodocumento.actual +1
            snumero = str(anumero).zfill(tipodocumento.longitud)
            snumero = tipodocumento.caracteres+snumero
            crea_cabeza_pedido_caja_registro_hotel(idcaja,idhabitacion,iduser,anumero,snumero,tipodocumento.id)
            crea_cuerpo_pedido_caja_registro_hotel(item.id,snumero,registro.valor_pago)
            pedido_caja_detalle = PedidoCajaDetalle.objects.get(numero=snumero)
            
            recibo_caja_detalle.numero = cnumero
            recibo_caja_detalle.IdTipoDocumento_id = tipodocumento.id 
            recibo_caja_detalle.IdReciboCaja_id = recibo_caja.id
            recibo_caja_detalle.IdPedidoCajaDetalle_id = pedido_caja_detalle.id
            recibo_caja_detalle.pedido_caja = cnumero
            recibo_caja_detalle.IdItem_id = item.id
            recibo_caja_detalle.valor = registro.valor_pago
            recibo_caja_detalle.cantidad = 1
            recibo_caja_detalle.valor_total = registro.valor_pago
            recibo_caja_detalle.save()
            recibo_caja_detalle.id += 1
            tot_val_rec = registro.valor_pago    
            RegistroHotel.objects.filter(id=idregistro).update(no_recibo_caja=cnumero,pagado=True) 
            ReciboCaja.objects.filter(numero=cnumero).update(valor=tot_val_rec)        
        return redirect('registros_list')
    else:
        mensaje1="No puede haber mas de un Item de Inventario marcado como estadia"
        mensaje2 = ''
        mensaje3 = ''
        return render(request,'hotel/mensaje_error_crea_recibo_caja_hotel.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3})            

def crea_cabeza_pedido_caja_registro_hotel(idcaja,idhabitacion,iduser,anumero,snumero,idtipodocumento):
    caja = Caja.objects.get(id=idcaja)
    mesa = Mesa.objects.get(idMesa='*')
    tipoingreso = TipoIngresoCaja.objects.get(idTipoIngreso='01')
    sucursal_defecto = ValorDefecto.objects.get(idValor='01')
    sucursal =Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
    pedido_caja = PedidoCaja()
    pedido_caja.numero = snumero 
    pedido_caja.fecha = timezone.now()    
    pedido_caja.IdTipoingreso_id = tipoingreso.id 
    pedido_caja.recibo_caja=''
    pedido_caja.estado = True
    pedido_caja.IdTipodocumento_id=idtipodocumento
    pedido_caja.IdMesa_id = mesa.id
    pedido_caja.IdHabitacion_id = idhabitacion
    pedido_caja.IdCaja_id = idcaja
    pedido_caja.IdSucursal_id = sucursal.id
    pedido_caja.IdUsuario_id = iduser
    pedido_caja.cerrado=True
    pedido_caja.save()
    TipoDocumentoCaja.objects.filter(idTipo='01').update(actual=anumero)

def crea_cuerpo_pedido_caja_registro_hotel(item,snumero,valor):
    detalle_pedido = PedidoCajaDetalle()
    pedido = PedidoCaja.objects.get(numero=snumero)        
    idtipodoc = TipoDocumentoCaja.objects.get(idTipo='01')
    detalle_pedido.numero = snumero
    detalle_pedido.IdTipoDocumento_id = idtipodoc.id
    detalle_pedido.IdPedidoCaja_id = pedido.id
    detalle_pedido.IdItem_id = item
    detalle_pedido.valor = valor
    detalle_pedido.cantidad = 1
    detalle_pedido.valor_total = valor
    detalle_pedido.save()
    PedidoCaja.objects.filter(numero=snumero).update(valor_total=valor)
                                  
def ValidaBorradoReciboCajaHotelView(request,id):
    request.session['idrecibocaja'] = id
    idrecibocaja = id
    if ReciboCaja.objects.filter(id=idrecibocaja,pagado=True):
        recibo_caja = ReciboCaja.objects.get(id=idrecibocaja)
        idcaja = recibo_caja.IdCaja_id
        pago = PagoReciboCaja.objects.get(recibo_caja=recibo_caja.numero)
        mensaje1="No se puede borrar porque tiene Pago,"
        mensaje2 = 'Debe anular el pago No. '+pago.numero+' '
        mensaje3 = 'para poder borrar el recibo de caja'
        return render(request,'hotel/mensaje_error_borrar_recibo_caja_hotel.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'idrecibocaja':idrecibocaja})            
    else:
        mensaje1="Esta seguro de borrar este recibo de caja?"
        mensaje2 = ''
        mensaje3 = ''
        return render(request,'hotel/mensaje_confirma_borra_recibo_caja_hotel.html',{'mensaje1':mensaje1,'idrecibocaja':idrecibocaja})

def BorraReciboCajaHotelView(request,id):
    idrecibocaja = request.session['idrecibocaja']
    idcaja = request.session['idcaja']
    if id == 1:
        recibo_caja = ReciboCaja.objects.get(id=idrecibocaja)
        no_registro = recibo_caja.registro
        PedidoCaja.objects.filter(recibo_caja=recibo_caja.numero).update(recibo_caja='',cerrado=False)
        RegistroHotel.objects.filter(consecutivo=recibo_caja.registro).update(no_recibo_caja='')
        valor_defecto = ValorDefecto.objects.get(idValor='08')
        if valor_defecto.valor == 1:
            ReciboCajaDetalle.objects.filter(numero=recibo_caja.numero).delete()
            ReciboCaja.objects.filter(id=idrecibocaja).delete()
        else:
            habitacion = Habitacion.objects.get(idHabitacion='*')
            mesa = Mesa.objects.get(idMesa='*')
            ReciboCaja.objects.filter(id=idrecibocaja).update(detalle='Recibo Anulado',valor=0,IdCaja_id=idcaja,pagado=0,IdMesa_id=mesa.id,IdHabitacion_id=habitacion.id,registo='')
            ReciboCajaDetalle.objects.filter(numero=recibo_caja.numero).delete()
    return redirect('recibo_caja_hotel')
        
class PagoEstadiaView(LoginRequiredMixin,CreateView):
    model = PagoReciboCaja
    template_name = 'hotel/pago_caja_hotel_form.html'
    form_class = PagoReciboCajaForm
    
    def get_initial(self,*args,**kwargs):
        idregistro =self.request.session['idregistro']
        registro = RegistroHotel.objects.get(id=idregistro)
        recibo_caja = ReciboCaja.objects.get(registro=registro.consecutivo,valor__gt=0)
        initial=super(PagoEstadiaView,self).get_initial(**kwargs)
        initial['recibo_caja'] = recibo_caja.numero
        initial['valor'] = recibo_caja.valor
        initial['IdTipoPago'] = 2  
        return initial
    
    def get_success_url(self):
        return reverse_lazy('busca_pago_hotel',self.kwargs['id'])   

    def form_valid(self, form):
        if form.is_valid():
            idregistro =self.request.session['idregistro']
            registro = RegistroHotel.objects.get(id=idregistro)
            recibo_caja_pagar = ReciboCaja.objects.get(registro=registro.consecutivo,valor__gt=0)
            sucursal_defecto = ValorDefecto.objects.get(idValor='01')
            tipodocumento = TipoDocumentoCaja.objects.get(idTipo='04')
            anumero = tipodocumento.actual +1
            snumero = str(anumero).zfill(tipodocumento.longitud)
            snumero = tipodocumento.caracteres+snumero
            pago_caja = form.save(commit=False)
            IdTipoPago = form.cleaned_data['IdTipoPago']
            IdTarjetaCredito = form.cleaned_data['IdTarjetaCredito']
            recibo_caja = form.cleaned_data['recibo_caja']
            detalle = form.cleaned_data['detalle']
            valor = form.cleaned_data['valor']
            idrecibocaja = recibo_caja_pagar.id
            idcaja = recibo_caja_pagar.IdCaja_id
                        
            pago_caja.fecha = timezone.now()
            pago_caja.numero = snumero   
            pago_caja.IdTercero_id = recibo_caja_pagar.IdTercero_id
            pago_caja.IdTipoDocumento_id = tipodocumento.id
            pago_caja.IdSucursal_id = sucursal_defecto.id
            pago_caja.IdUsuario_id = self.request.user.id
            pago_caja.IdCaja_id = idcaja 
            pago_caja.recibo_caja = recibo_caja_pagar.numero
            pago_caja.estado = 1
            pago_caja.save()
            pago_caja.id += 1
            idregistro = self.request.session['idregistro']
            ReciboCaja.objects.filter(numero=recibo_caja_pagar.numero).update(pagado=True)
            TipoDocumentoCaja.objects.filter(idTipo='04').update(actual = anumero )
            RegistroHotel.objects.filter(id=idregistro).update(pagado=True) 
            return redirect('recibo_caja_hotel')


def AcompañanteHotelListaView(request,id):
    idregistro = id
    if AcompañanteHotel.objects.filter(IdRegistro_id=idregistro):
        acompañantes = AcompañanteHotel.objects.filter(IdRegistro_id=idregistro)
        acompañantes = AcompañanteHotelTable(acompañantes)
        acompañantes.paginate(page=request.GET.get("page", 1), per_page=8)
        idregistro=request.session['idregistro']
        context = {'acompañantes':acompañantes,'idregistro':idregistro}
    else:
        return redirect('crea_acompañante_hotel',idregistro)   
     
    return render(request, 'hotel/acompañante_hotel_list.html', context)

class EditaAcompañanteHotelView(LoginRequiredMixin,UpdateView):
    model = AcompañanteHotel
    fields = ['identificacion','IdTipoIdentificacion','identifica_de','apenom','lugar_residencia']
    template_name = 'hotel/acompañante_hotel_form.html'
    #success_url = reverse_lazy('acompañante_hotel_list')

    def get_success_url(self, *args, **kwargs):
        idregistro = self.request.session['idregistro']
        return reverse_lazy('acompañante_hotel_list', kwargs={'id': idregistro})

def CreaAcompañanteHotelDetalleView(request):
    idregistro = request.session['idregistro']
    if RegistroHotel.objects.filter(id=idregistro).exists():
        return redirect('crea_acompañante_hotel',pk=idregistro)    
    return redirect('registros_list.html')    

class CreaAcompañanteHotelView(LoginRequiredMixin,CreateView):
    model = AcompañanteHotel
    template_name = 'hotel/acompañante_hotel_form.html'
    form_class = AcompañanteHotelForm
    
    def get_success_url(self):
        idregistro = self.object.id
        self.request.session['idregistro' ] = idregistro
        return redirect('acompañante_hotel_list')   

    def form_valid(self, form):
        idregistro = self.request.session['idregistro' ]
        if form.is_valid():
            acompañante_hotel = form.save(commit=False)
            acompañante_hotel.IdRegistro_id = idregistro
            acompañante_hotel.save()
            return redirect('acompañante_hotel_list',idregistro)

def TerceroEditView(request,id):
    registro = RegistroHotel.objects.get(id=id)
    tercero = Tercero.objects.get(id=registro.IdTercero_id)
    return redirect('revisa_tercero',pk=tercero.id)

class RevisaTerceroView(LoginRequiredMixin,UpdateView):
    model = Tercero
    fields = ['identificacion','IdTipoIdentificacion','identifica_de','nombre1','nombre2','apel1','apel2','razon_social','IdPais','departamento','ciudad','ocupacion',
                  'direccion','telefono','email','direccion','telefono']
    template_name = 'hotel/tercero_registro_hotel_form.html'
    
    def get_success_url(self, *args, **kwargs):
        idregistro = self.request.session['idregistro']
        return reverse_lazy('registro_detalle_list', kwargs={'id': idregistro})
        

class BorraAcompañanteView(LoginRequiredMixin,DeleteView):
    model = AcompañanteHotel
    template_name = 'hotel/confirma_borrado.html'

    def get_success_url(self):
        idregistro = self.request.session['idregistro' ] 
        return reverse_lazy('acompañante_hotel_list',args=[idregistro])

def View(self,id):
    AcompañanteHotel.objects.filter(id=id).delete()
    idregistro = self.request.session['idregistro' ] 
    return redirect('acompañante_hotel_list',args=[idregistro])


""" def P(txt):
    return Paragraph(txt, style)

style = ParagraphStyle(
    name='Normal',
    fontSize=7,
    ) """

def PoneProductoFormula(request,id):
    items = MaestroItem.Objects.filter()

    y = 0
    #cuerpo = SolicitudDetalle.objects.filter(solicitud_id=cabeza.id)
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    y = 800
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(170, y, u""+empresa.nombre.strip())
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(160, y, u"RECIBO DE CAJA")
    pdf.setFont("Helvetica", 9)
    recibos = ReciboCaja.objects.filter(id=id)    
    for i in recibos: 
        cuerpo = ReciboCajaDetalle.objects.filter(numero=i.numero)
        x = 380
        factor = 15
        baja = 5
        y -= 10
        pdf.line(30,y,x,y)
        y -= baja+5
        pdf.drawString(30,y , u"Número : "+str(i.numero))
        pdf.drawString(180,y , u"Fecha : "+i.created.strftime("%Y-%m-%d %H:%M:%S"))
        y -= baja
        pdf.line(30,y,x,y)
        y -= baja
        y -= factor
        pdf.drawString(30, y, u"Cliente : "+str(i.IdTercero))
        y -= factor
        pdf.drawString(30, y, u"Pedido Caja : "+str(i.pedido_caja))
        y -= factor
        pdf.drawString(30, y, u"Habitación   : "+str(i.IdHabitacion))
        y -= factor
        pdf.drawString(30, y, u"Mesa : "+str(i.IdMesa))
        y -= factor
        y -= baja
        #y = 760
        cuerpo = ReciboCajaDetalle.objects.filter(numero=i.numero)
        total_recibo = cuerpo.aggregate(Sum('valor_total'))['valor_total__sum']
        total = total_recibo
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Producto', 'Cantidad', 'Valor Unit.', 'Valor Total')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(cuerpo.IdItem.descripcion[0:35], cuerpo.cantidad, '{:,}'.format(cuerpo.valor), '{:,}'.format(cuerpo.valor_total)) for cuerpo in cuerpo]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_recibo = Table([encabezados] + detalles, colWidths=[5 * cm, 2 * cm, 2.5 * cm, 2.5 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_recibo.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1), 7),
        ]
        ))
        b= 0
        for a in cuerpo:
            b += 1
        y = y -b*18    
        if y<=30:
            pdf.showPage()
            y= 680    
        # Descontamos el encabezado
        #y = y - 80
        # Restamos a y por cada fila de la grid
        #y = y - b*18
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_recibo.wrapOn(pdf, 300, 800)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_recibo.drawOn(pdf, 30,y)
        y -= 10
        if total_recibo:
            pdf.setFont("Helvetica", 9)
            pdf.drawString(240, y, u"Total Recibo      : "+('{:,}'.format(total_recibo)+'.00'))
        y -= 20
        
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response         

def ImpresionPagoReciboCajaHotelView(request,id):
    y = 0
    response = HttpResponse(content_type='application/pdf')
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    y = 800
    #pdf.setFont("Helvetica", 16)
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(210, y, u""+empresa.nombre)
    #pdf.setFont("Helvetica", 14)
    y -= 25
    pdf.drawString(250, y, u"PAGOS")
    #pdf.setFont("Helvetica", 9)
    pagos = PagoReciboCaja.objects.filter(id=id)    
    #y -= 10
    y -= 20
    encabezados = ('Número','Fecha','Detalle','Caja','Cliente','Rec. Caja','Tipo Pago','Tarjeta Cred.','Valor')
    detalle = [(pago.numero, pago.fecha,P(pago.detalle),P(pago.IdCaja.descripcion),P(pago.IdTercero.nombre),pago.recibo_caja,P(pago.IdTipoPago.descripcion),P(pago.IdTarjetaCredito.descripcion),'{:,}'.format(pago.valor)) for pago in pagos]
    detalle_pago = Table([encabezados] + detalle, colWidths=[1.4 * cm, 1.5 * cm, 3 * cm, 1.8 * cm,cm * 6,cm * 1.3,cm* 2,cm * 1.8,cm * 1.8 ])
    detalle_pago.setStyle(TableStyle(
    [
        #La primera fila(encabezados) va a estar centrada
        ('ALIGN',(0,0),(3,0),'CENTER'),
        #Los bordes de todas las celdas serán de color negro y con un grosor de 1
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        #El tamaño de las letras de cada una de las celdas será de 10
        ('FONTSIZE', (0, 0), (-1, -1),7),
    ]
    ))
    total_pagos = pagos.aggregate(Sum('valor'))['valor__sum']
    b= 0
    for j in detalle:
        b += 1
    y = y - b*33
    if y<= 35:
        pdf.showPage()
        y= 700
    print('Valor y :',y)
    detalle_pago.wrapOn(pdf, 300, 800)
    detalle_pago.drawOn(pdf, 5,y)
    y -= 10
    if total_pagos:
        pdf.setFont("Helvetica", 9)
        pdf.drawString(470, y, u"Total Pagos      : "+('{:,}'.format(total_pagos)+'.00'))
    y -= 20
    #Con show page hacemos un corte de página para pasar a la siguiente
    y = 455
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def ImpresionGruposInventarioXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
        
    worksheet.write('A1','Id' )
    worksheet.write('B1','Descripción' )
    grupos = Grupo.objects.all()
    n=2
    for j in grupos:     
        nn = str(n)
        id = j.idGrupo
        descripcion = j.descripcion
        exec("worksheet.write('A"+nn+"','"+id+"' )")
        exec("worksheet.write('B"+nn+"','"+descripcion+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'grupos_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    

def ImpresionHabitacionesPdfView(request):
    grupos = Habitacion.objects.all().order_by('id')
    y = 0
    response = HttpResponse(content_type='application/pdf')
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    y = 800
    #pdf.setFont("Helvetica", 16)
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(210, y, u""+empresa.nombre)
    #pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(200, y, u"HABITACIONES")
    pdf.setFont("Helvetica", 9)
    y -= 90
    habitaciones = Habitacion.objects.all()
    encabezados = ('Código','Descripción','Valor Noche','Tipo Habitación')
    detalle = [(habitacion.idHabitacion, habitacion.descripcion[0:30],habitacion.valor_noche,habitacion.IdTipoHabitacion.descripcion) for habitacion in habitaciones]
    detalle_table = Table([encabezados] + detalle, colWidths=[1.5 * cm, 6 * cm,2 * cm,6 * cm])
    detalle_table.setStyle(TableStyle(
    [
        #La primera fila(encabezados) va a estar centrada
        ('ALIGN',(0,0),(3,0),'CENTER'),
        #Los bordes de todas las celdas serán de color negro y con un grosor de 1
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        #El tamaño de las letras de cada una de las celdas será de 10
        ('FONTSIZE', (0, 0), (-1, -1),7),
    ]
    ))
    b= 0
    for j in detalle:
        b += 1
    y = y - b*18
    if y<= 35:
        pdf.showPage()
        y= 700
    detalle_table.wrapOn(pdf, 300, 800)
    detalle_table.drawOn(pdf, 40,y)
    y -= 10
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionHabitacionesXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
        
    worksheet.write('A1','Código' )
    worksheet.write('B1','Descripción' )
    worksheet.write('C1','Valor Noche' )
    worksheet.write('D1','Grupo' )
    habitaciones = Habitacion.objects.all()   
    n=2
    for j in habitaciones:     
        nn = str(n)
        id = j.idHabitacion
        descripcion = j.descripcion
        exec("worksheet.write('A"+nn+"','"+id+"' )")
        exec("worksheet.write('B"+nn+"','"+descripcion+"' )")
        exec("worksheet.write('C"+nn+"','"+str(j.valor_noche)+"' )")
        tipo_habitacion = TipoHabitacion.objects.get(id=j.IdTipoHabitacion_id)
        exec("worksheet.write('D"+nn+"','"+tipo_habitacion.descripcion+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'habitaciones.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    


def ImpresionRegistrosHotelView(request):
    y = 0
    #cuerpo = SolicitudDetalle.objects.filter(solicitud_id=cabeza.id)
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    y = 800
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(170, y, u""+empresa.nombre)
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(200, y, u"REGISTRO HOTEL")
    pdf.setFont("Helvetica", 9)
    lista_id_registros= request.session['lista_id_filtro_registros_hotel']
    if request.session['lista_id_filtro_registros_hotel']:
        id_registros = request.session['lista_id_filtro_registros_hotel']
        registros = ReciboCaja.objects.filter(id__in=id_registros)
    else:
        registros = ReciboCaja.objects.all()    
    for i in registros: 
        x = 380
        factor = 15
        baja = 5
        y -= 10
        pdf.line(30,y,x,y)
        y -= baja+5
        'IdHabitacion','IdTercero','check_in','hora_check_in','check_out','hora_check_out','no_de_noches','valor_pago','pagado'
        'consecutivo','descripcion','tarifa_habitacion','ocupacion','empresa','motivo_viaje','procedencia','destino','placa_vehiculo','dias_estadia',
        'no_adultos','no_niños','equipaje','pagado','no_recibo_caja'
        pdf.drawString(30,y , u"Cliente : "+str(i.numero))
        pdf.drawString(180,y , u"Fecha : "+i.created.strftime("%Y-%m-%d %H:%M:%S"))
        y -= baja
        pdf.line(30,y,x,y)
        y -= baja
        y -= factor
        pdf.drawString(30, y, u"Cliente : "+str(i.IdTercero))
        y -= factor
        pdf.drawString(30, y, u"Pedido Caja : "+str(i.pedido_caja))
        y -= factor
        pdf.drawString(30, y, u"Habitación   : "+str(i.IdHabitacion))
        y -= factor
        pdf.drawString(30, y, u"Mesa : "+str(i.IdMesa))
        y -= factor
        y -= baja
        #y = 760
        cuerpo = ReciboCajaDetalle.objects.filter(numero=i.numero)
        total_recibo = cuerpo.aggregate(Sum('valor_total'))['valor_total__sum']
        total = total_recibo
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Producto', 'Cantidad', 'Valor Unit.', 'Valor Total')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(cuerpo.IdItem, cuerpo.cantidad, '{:,}'.format(cuerpo.valor), '{:,}'.format(cuerpo.valor_total)) for cuerpo in cuerpo]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_recibo = Table([encabezados] + detalles, colWidths=[5 * cm, 2 * cm, 2.5 * cm, 2.5 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_recibo.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1), 7),
        ]
        ))
        b= 0
        for a in cuerpo:
            b += 1
        y = y -b*18    
        if y<=30:
            pdf.showPage()
            y= 680    
        # Descontamos el encabezado
        #y = y - 80
        # Restamos a y por cada fila de la grid
        #y = y - b*18
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_recibo.wrapOn(pdf, 300, 800)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_recibo.drawOn(pdf, 30,y)
        y -= 10
        if total_recibo:
            pdf.setFont("Helvetica", 9)
            pdf.drawString(240, y, u"Total Recibo      : "+('{:,}'.format(total_recibo)+'.00'))
        y -= 20
        
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


def ImpresionFormatoRegistroHotelView(request,id):
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    y = 800
    #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
    archivo_imagen = settings.STATIC_ROOT+'/img/logo_empresa.png'
    #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
    y = y -30
    pdf.drawImage(archivo_imagen, 1, y-50, 100, 70,preserveAspectRatio=True)
    #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 20)
    #Dibujamos una cadena en la ubicación X,Y especificada
    a = 15
    registro = RegistroHotel.objects.get(id=id)
    pdf.setFont("Times-Roman", 20)
    pdf.drawString(80, y+15, u"HOTEL CAMPESTRE LOS ARRAYANES")
    #pdf.line(5,y-a,595,y-a)
    pdf.line(464,y+30,585,y+30)
    pdf.line(464,y+10,585,y+10)

    pdf.line(465,y+30,465,y+10)
    pdf.line(495,y+30,495,y+10)
    pdf.line(535,y+30,535,y+10)
    pdf.line(586,y+30,586,y+10)
    dia = date.today().day
    mes = date.today().month
    pdf.drawString(470, y+13, u""+str(dia).zfill(2)+"   "+str(mes).zfill(2)+"   "+str(date.today().year))
    y = y-a
    #pdf.line(5,y-a,595,y-a)
    pdf.setFont("Helvetica", 14)
    y = y-a
    pdf.drawString(170, y+24, u"Hotel km 5 Vía Moniquirá-Barbosa"+"           ")
    y = y-a
    pdf.setFont("Helvetica", 12)
    pdf.drawString(170, y+13, u"Cel. 312 457 43 65 - 312 457 43 64                 Tarjeta de Registro")
    y = y-a
    pdf.drawString(415, y+15, u" Hotelero")
    pdf.setFont("Times-Roman", 20)
    pdf.drawString(490, y+5, u""+registro.consecutivo)
    y = y-5
    pdf.line(5,y,575,y)
    #Línea vertical
    pdf.line(6,y,6,y-a-210)
    pdf.line(200,y,200,y-a-110)
    pdf.line(400,y,400,y-a-110)
    pdf.line(575,y,575,y-a-210)
    
    y = y-a
    pdf.setFont("Helvetica", 12)
    pdf.drawString(75,y, u"NOMBRE/NAME")
    pdf.drawString(210,y, u"NACIONALIDAD/NATIONALITY")
    pdf.drawString(440,y, u"IDENTIFICACION/I.D")
    pdf.setFont("Helvetica", 9)
    pdf.line(5,y-4,575,y-4)
    y = y-a
    pdf.drawString(10,y, u""+registro.IdTercero.apenom[0:30])
    pdf.drawString(220,y, u""+registro.nacionalidad)
    tercero = Tercero.objects.get(id=registro.IdTercero_id)
    tipo_identificacion = TipoIdentificacion.objects.get(id=tercero.IdTipoIdentificacion_id)
    pdf.setFont("Helvetica", 7)
    pdf.drawString(405,y, u""+tipo_identificacion.descripcion)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(510,y, u""+registro.IdTercero.identificacion)
    pdf.drawString(600,y, u"De/From "+registro.IdTercero.identifica_de)
    pdf.line(5,y-4,575,y-4)
    y = y-a
    pdf.drawString(10,y, u"")
    pdf.drawString(220,y, u"")
    pdf.drawString(445,y, u"")
    pdf.drawString(600,y, u"De/From ")
    pdf.line(5,y-4,575,y-4)
    y = y-a
    pdf.drawString(10,y, u"")
    pdf.drawString(220,y, u"")
    pdf.drawString(445,y, u"")
    pdf.drawString(600,y, u"De/From ")
    pdf.line(5,y-4,575,y-4)
    y = y-a
    pdf.drawString(10,y, u"")
    pdf.drawString(220,y, u"")
    pdf.drawString(445,y, u"")
    pdf.drawString(600,y, u"De/From ")
    pdf.line(5,y-4,575,y-4)

    pdf.setFont("Helvetica", 10)
    pdf.drawString(75,y, u"DIRECCION")
    pdf.drawString(230,y, u"CIUDAD")
    pdf.line(300,y+12,300,y-20)
    pdf.drawString(330,y, u"PAIS")
    pdf.drawString(410,y, u"TELEFONO")
    pdf.line(467,y+12,467,y-20)
    pdf.drawString(470,y, u"OFICIO/OCUPACION")
    pdf.setFont("Helvetica", 9)
    y = y-a
    pdf.drawString(8,y, u""+registro.IdTercero.direccion)
    pdf.drawString(215,y, u""+registro.IdTercero.ciudad)
    pdf.drawString(335,y, u""+registro.IdTercero.IdPais.descripcion)
    pdf.drawString(401,y, u""+registro.IdTercero.telefono[0:13])
    pdf.drawString(470,y, u""+registro.ocupacion)
    pdf.line(5,y-4,575,y-4)
    y = y-a
    pdf.setFont("Helvetica", 10)
    pdf.drawString(75,y, u"EMPRESA")
    pdf.drawString(260,y, u"TELEFONO")
    pdf.drawString(440,y, u"EMAIL")
    pdf.line(5,y-4,575,y-4)
    y = y-a
    pdf.setFont("Helvetica",9)
    pdf.drawString(10,y, u""+registro.IdTercero.razon_social)
    pdf.drawString(265,y, u""+registro.IdTercero.telefono)
    tercero = Tercero.objects.get(id = registro.IdTercero_id)
    pdf.drawString(410,y, u""+str(tercero.email))
    pdf.line(5,y-4,575,y-4)
    y = y-a
    pdf.drawString(150,y, u"OTROS ACOMPAÑANTES")
    pdf.setFont("Helvetica", 6)
    pdf.drawString(351,y, u"MOTIVO VIAJE")
    pdf.drawString(351,y-7, u"PORPOUSE OF TRIP")
    pdf.line(5,y-10,350,y-10)
    y = y-a-6
    pdf.setFont("Helvetica", 9)
    pdf.drawString(50,y, u"NOMBRE")
    pdf.drawString(145,y, u"CEDULA")
    pdf.drawString(245,y, u"LUGAR DE RESIDENCIA")
    pdf.line(5,y-6,350,y-6)
    acompañantes = AcompañanteHotel.objects.filter(IdRegistro_id=id)
    pdf.setFont("Helvetica",8)
    pdf.line(6,y+10,6,y-50)
    pdf.line(130,y+10,130,y-50)
    pdf.line(240,y+10,240,y-50)
    pdf.line(350,y+31,350,y-50)
    y = y-a
    s = 0
    for l in acompañantes:
        pdf.drawString(8,y-s, u""+l.apenom)
        pdf.drawString(135,y-s, u""+l.identificacion)
        pdf.drawString(245,y-s, u""+l.lugar_residencia)
        s = s + 15
        #pdf.line(5,y-5,350,y-5)
    y = y - 45
    if registro.motivo_viaje == '1' :
       pdf.drawString(360,y+58, u"Recreación")
       pdf.drawString(360,y+48, u"Recreation")
    if registro.motivo_viaje == '2' :
       pdf.drawString(360,y+58, u"Negocios")
       pdf.drawString(360,y+48, u"Business")
    if registro.motivo_viaje == '3' :
       pdf.drawString(360,y+58, u"Salud")
       pdf.drawString(360,y+48, u"Health")
    if registro.motivo_viaje == '4' :
       pdf.drawString(360,y+58, u"Otros")
       pdf.drawString(360,y+48, u"Others")
    
    pdf.line(410,y+92,410,y+9)
    pdf.line(490,y+92,490,y+38)
    pdf.line(575,y+92,575,y+9)

    pdf.line(410,y+10,410,y-10)

    pdf.setFont("Helvetica", 6)
    pdf.drawString(415,y+85, u"PROCEDENCIA")
    pdf.drawString(415,y+78, u"COMMING FROM")
    
    pdf.drawString(495,y+85, u"ESTADIA/STAY")
    pdf.drawString(495,y+78, u"DIAS/DAYS")
    pdf.setFont("Helvetica", 7)
    pdf.drawString(418,y+69, u""+registro.procedencia)
    pdf.drawString(497,y+69, u""+str(registro.dias_estadia))
    
    pdf.line(410,y+65,575,y+65)

    pdf.setFont("Helvetica", 6)
    pdf.drawString(415,y+55, u"DESTINO/DESTINATION")
    pdf.drawString(495,y+55, u"PLACA AUTOMOVIL")
    pdf.setFont("Helvetica", 7)
    pdf.drawString(418,y+45, u""+registro.destino)
    pdf.drawString(497,y+45, u""+str(registro.placa_vehiculo))
    
    pdf.setFont("Helvetica", 6)
    pdf.drawString(415,y+30, u"FIRMA/SIGNATURE")
    pdf.setFont("Helvetica", 5)
    pdf.drawString(415,y+25, u"Acepto Contrato de Hospedaje/Accept Accomodation Contract")

    pdf.line(6,y+40,575,y+40)
    pdf.line(6,y+25,351,y+25)
    pdf.line(6,y+9,575,y+9)

    tarifa = float(registro.tarifa_habitacion)

    pdf.setFont("Helvetica", 7) 
    pdf.drawString(415,y, u"TARIFA HABITACION/RATE")
    pdf.drawString(518,y, u""+'{:,}'.format(tarifa)+" Noche")
    pdf.line(6,y-25,575,y-25)
    pdf.line(6,y-10,575,y-10)
    pdf.line(6,y-45,575,y-45)
    pdf.setFont("Helvetica", 7)
    pdf.drawString(10,y, u"Firma Recepcionista")
    
    #pdf.line(6,y-10,6,y-40)
    #pdf.line(575,y-10,575,y-40)
    pdf.setFont("Helvetica", 7)
    pdf.drawString(200,y-40, u"PARA USO DEL HOTEL / FOR HOTEL USE ONLY")
    y = y - 80
    pdf.line(6,y,575,y)
    pdf.line(6,y+55,6,y-1)
    pdf.line(575,y+55,575,y-1)
    
    pdf.setFont("Helvetica", 8)
    pdf.drawString(9,y+20, u"Habitación No.")
    pdf.setFont("Helvetica", 7)
    pdf.drawString(9,y+10, u""+registro.IdHabitacion.descripcion)
    pdf.line(115,y+35,115,y-1)
    pdf.line(145,y+13,145,y-1)

    pdf.drawString(123,y+25, u"OCUPANTES")
    pdf.drawString(119,y+15, u"Adultos")
    pdf.drawString(150,y+15, u"Niños")
    pdf.drawString(130,y+5, u""+str(registro.no_adultos))
    pdf.drawString(160,y+5, u""+str(registro.no_ninos))
    pdf.line(180,y+35,180,y-1)
    
    pdf.drawString(200,y+25, u"ENTRADA")
    pdf.line(260,y+35,260,y-1)
    pdf.drawString(280,y+25, u"SALIDA")

    pdf.line(208,y+10,208,y-1)
    pdf.line(230,y+10,230,y-1)
    pdf.drawString(187,y+15, u"Dia")
    pdf.drawString(210,y+15, u"Mes")
    pdf.drawString(235,y+15, u"Año")
    dia = str(registro.check_in.day)
    mes = str(registro.check_in.month)
    pdf.drawString(190, y+5, u""+str(dia.zfill(2))+"          "+str(mes.zfill(2))+"         "+str(registro.check_in.year))

    pdf.line(285,y+10,285,y-1)
    pdf.line(305,y+10,305,y-1)
    pdf.drawString(270,y+15, u"Dia")
    pdf.drawString(290,y+15, u"Mes")
    pdf.drawString(310,y+15, u"Año")
    dia = str(registro.check_out.day)
    mes = str(registro.check_out.month)
    pdf.drawString(270, y+5, u""+str(dia.zfill(2))+"         "+str(mes.zfill(2))+"      "+str(registro.check_out.year))
    pdf.line(340,y+35,340,y-1)

    pdf.drawString(350,y+25, u"EQUIPAJE")
    pdf.line(340,y+35,340,y-1)
    pdf.drawString(360,y+5, u""+str(registro.equipaje))
    pdf.drawString(420,y+25, u"FORMA DE PAGO")
    pdf.line(410,y+35,410,y-1)

    if PagoReciboCaja.objects.filter(recibo_caja=registro.no_recibo_caja).exists():
        pago_caja = PagoReciboCaja.objects.get(recibo_caja=registro.no_recibo_caja)
        pdf.drawString(450,y+5, u""+str(pago_caja.IdTipoPago.descripcion))
    
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionReservasPdfView(request):
    y = 0
    #cuerpo = SolicitudDetalle.objects.filter(solicitud_id=cabeza.id)
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    y = 800
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(170, y, u""+empresa.nombre)
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(200, y, u"RESERVAS HOTEL")
    pdf.setFont("Helvetica", 9)
    id_registros = request.session['lista_id_filtro_reservas_hotel']
    if request.session['lista_id_filtro_reservas_hotel']:
        id_reservas = request.session['lista_id_filtro_reservas_hotel']
        reservas = ReservaHabitacion.objects.filter(id__in=id_registros)
    else:
        reservas = RegistroHotel.objects.all()    
    for i in reservas: 
        x = 500
        factor = 15
        baja = 10
        y -= 10
        pdf.line(30,y,x,y)
        y -= baja+5
        pdf.drawString(30,y , u"Consecutivo : "+i.consecutivo)
        pdf.drawString(200,y , u"Fecha Reserva : "+i.fecha_reserva.strftime("%Y-%m-%d %H:%M:%S"))
        y -= baja
        pdf.drawString(30,y , u"Fecha Ingreso : "+i.fecha_ingreso.strftime("%Y-%m-%d %H:%M:%S"))
        pdf.drawString(200,y , u"Fecha Salida : "+i.fecha_salida.strftime("%Y-%m-%d %H:%M:%S"))
        y -= baja
        pdf.drawString(30, y, u"Cliente : "+i.nombre_reserva)
        pdf.drawString(130, y, u"Habitación : "+i.IdHabitacion.descripcion)
        pdf.drawString(350, y, u"No. Noches   : "+str(i.no_de_noches))
        y -= baja
        pdf.drawString(30, y, u"Descripción : "+str(i.descripcion))
        y -= baja
        pdf.line(30,y,x,y)
        if y<=30:
            pdf.showPage()
            y= 680    
                   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

#IdHabitacion,consecutivo,descripcion,fecha_ingreso,fecha_salida,fecha_reserva,valor_reserva,telefono,nombre_reserva,email,pin,no_de_dias,no_de_noches,IdSucursal,

def ImpresionReservasXlsView(request):
    #idrecibos = request.session['lista_id_filtro_recibo_caja']
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    #recibos_detalle = ReciboCajaDetalle.objects.filter(id=idsesionempaque)
    
    worksheet.write('A1','Consecutivo' )
    worksheet.write('B1','Habitación' )
    worksheet.write('C1','Nombre')
    worksheet.write('D1','Fecha Reserva')
    worksheet.write('E1','Fecha Ingreso')
    worksheet.write('F1','Fecha Salida')
    worksheet.write('G1','Email')
    worksheet.write('H1','Teléfono')
    worksheet.write('I1','Número Días')
    worksheet.write('J1','Número Noches')
    id_registros = request.session['lista_id_filtro_reservas_hotel']
    n = 2
    if request.session['lista_id_filtro_reservas_hotel']:
        id_reservas = request.session['lista_id_filtro_reservas_hotel']
        reservas = ReservaHabitacion.objects.filter(id__in=id_registros)
    else:
        reservas = RegistroHotel.objects.all()    
    for j in reservas: 
        nn = str(n)
        habitacion = j.IdHabitacion.descripcion
        fecha_reserva = j.fecha_reserva.strftime("%d/%m/%Y")
        fecha_ingreso = j.fecha_ingreso.strftime("%d/%m/%Y")
        fecha_salida = j.fecha_salida.strftime("%d/%m/%Y")
        exec("worksheet.write('A"+nn+"','"+j.consecutivo+"' )")
        exec("worksheet.write('B"+nn+"','"+habitacion+"' )")
        exec("worksheet.write('C"+nn+"','"+j.nombre_reserva+"' )")
        exec("worksheet.write('D"+nn+"','"+str(fecha_reserva)+"' )")
        exec("worksheet.write('E"+nn+"','"+str(fecha_ingreso)+"' )")
        exec("worksheet.write('F"+nn+"','"+str(fecha_salida)+"' )")
        exec("worksheet.write('G"+nn+"','"+j.email+"' )")
        exec("worksheet.write('H"+nn+"','"+j.telefono+"' )")
        exec("worksheet.write('I"+nn+"','"+str(j.no_de_dias)+"' )")
        exec("worksheet.write('I"+nn+"','"+str(j.no_de_noches)+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'reservas.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    
    """ pdf.line(480+b,y-a,480+b,880-a)
    pdf.line(480+b,y-a,597+b,800-a)
    pdf.line(480+b,y-a,597+b,820-a)
    pdf.setFont("Helvetica", 8)
    pdf.drawString(495+b,825-a, u"PRO-F-024")
    pdf.setFont("Helvetica", 8)
    pdf.drawString(490+b,807-a, u"Versión: 005")
    pdf.drawString(490+b,788-a, u"Página "+str(pagina))
    pdf.drawString(530+b,788-a, u"de "+str(total_paginas))
    proceso_limpieza = ProcesoLimpieza.objects.get(extraccion_id=idextraccion)
    extraccion = Extraccion.objects.get(id=idextraccion)
    donante = Donante.objects.get(id=extraccion.donante_id)
    y = 540
    pdf.drawString(10,y, u"DONANTE: "+donante.numero)
    pdf.drawString(100,y, u"LUGAR EXTRACCION: "+donante.lugar_ubicacion)
    if donante.lugar_ubicacion == 'RTB':
        pdf.drawString(250,y, u"RTB: _____X_____")
    else:
        pdf.drawString(250,y, u"RTB: ___________")
    if donante.lugar_ubicacion == 'INML':    
        pdf.drawString(350,y, u"INML: ____X_____")
    else:
        pdf.drawString(350,y, u"INML: __________")
    if donante.lugar_ubicacion == 'RTC':    
        pdf.drawString(450,y, u"RTC: ____X______")
    else:
        pdf.drawString(450,y, u"RTC: __________")
    if donante.lugar_ubicacion == 'IPS':    
        pdf.drawString(550,y, u"IPS: ____X__ _  ___")
    else:
        pdf.drawString(550,y, u"IPS: __________")        
    y -= 12
    pdf.drawString(250,y, u"EDAD: "+str(donante.edad))
    pdf.drawString(400,y, u"SEXO: "+donante.genero)
    y -= 12
    pdf.line(5,y,595+b,y)
    y -= 12
    pdf.drawString(250,y, u"DATOS PROCESO DE EXTRACCION")
    y -= 12
    pdf.line(5,y,595+b,y)
    y -= 12
    c= 50
    pdf.drawString(5+c,y, u"Fecha Extracción: "+extraccion.fecha_hora_inicio.strftime("%Y-%m-%d %H:%M:%S"))
    pdf.drawString(180+c,y,u"Técnico: "+str(extraccion.tecnico_lado_derecho)+" - "+str(extraccion.tecnico_lado_izquierdo))
    pdf.drawString(350+c,y,u"Técnico de Mesa: "+str(extraccion.tecnico_mesa))
    pdf.drawString(500+c,y,u"Circulante: "+str(extraccion.circulante))
    y -= 12
    pdf.line(5,y,595+b,y)
    y -= 12
    pdf.drawString(220+c,y, u"DATOS PROCESO DE LIMPIEZA")
    y -= 12
    pdf.line(5,y,595+b,y)
    y -= 12
    pdf.drawString(5+c,y, u"Fecha Limpieza: "+proceso_limpieza.fecha_hora_inicial.strftime("%Y-%m-%d %H:%M:%S"))
    pdf.drawString(180+c,y,u"Técnico: "+str(proceso_limpieza.tecnico_lado_derecho)+" - "+str(proceso_limpieza.tecnico_lado_izquierdo))
    pdf.drawString(400+c,y,u"Circulante: "+str(proceso_limpieza.circulante))
    y -= 12
    pdf.line(5,y,595+b,y)
    y -= 9
    pdf.line(5,y,595+b,y)
    inicio_horizontal = y
    y -= 40
    pdf.line(5,y,595+b,y)

    pdf.drawString(7,y+29, u"TIPO DE NOVEDAD")
    pdf.drawString(120+c,y+29, u"INJERTO")
    pdf.drawString(310+c,y+29, u"DESCRIPCION")
    pdf.drawString(495+c,y+30, u"INJERTO NO PROCESADO")
    pdf.drawString(698+c,y+29, u"CANTIDAD")
    return y,inicio_horizontal """

def ImpresionRegistroPdfView(request):
    y = 0
    #cuerpo = SolicitudDetalle.objects.filter(solicitud_id=cabeza.id)
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    y = 800
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(170, y, u""+empresa.nombre)
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(200, y, u"REGISTRO HOTEL")
    pdf.setFont("Helvetica", 9)
    lista_id_registros= request.session['lista_id_filtro_registros_hotel']
    if request.session['lista_id_filtro_registros_hotel']:
        id_registros = request.session['lista_id_filtro_registros_hotel']
        registros = RegistroHotel.objects.filter(id__in=id_registros)
    else:
        registros = RegistroHotel.objects.all()    
    for i in registros: 
        x = 530
        factor = 15
        baja = 10
        y -= 10
        pdf.line(30,y,x,y)
        y -= baja+5
        if i.IdTercero.razon_social=='' :
            tercero = i.IdTercero.apenom
        else:
            tercero = i.IdTercero.razon_social
        habitacion = i.IdHabitacion.descripcion
        pagado = i.pagado
        if pagado == True:
            pagado = 'Si'
        else:
            pagado = 'No'
        pdf.drawString(30,y , u"Habitación : "+habitacion)
        y -= baja    
        pdf.drawString(30,y , u"Cliente : "+tercero)
        y -= baja
        pdf.drawString(30,y , u"Check In : "+i.check_in.strftime("%Y-%m-%d %H:%M:%S"))
        pdf.drawString(180,y , u"Hora: "+i.hora_check_in.strftime("%H:%M:%S"))
        if i.check_out == None:
            pdf.drawString(250,y , u"Check Out : ")        
            pdf.drawString(400,y , u"Hora: ")
        else:    
            pdf.drawString(250,y , u"Check Out : "+i.check_out.strftime("%Y-%m-%d %H:%M:%S"))        
            pdf.drawString(400,y , u"Hora: "+i.hora_check_out.strftime("%H:%M:%S"))
        y -= baja
        pdf.drawString(30,y , u"Descripción : "+i.descripcion)
        y -= baja
        pdf.drawString(30,y , u"Tarifa Habitación : "+str(i.tarifa_habitacion))
        pdf.drawString(180,y , u"Valor Pago : "+str(i.valor_pago))
        pdf.drawString(400,y , u"Pagado : "+pagado)
        y -= baja
        pdf.drawString(30,y , u"Motivo Viaje : "+i.motivo_viaje)
        pdf.drawString(180,y , u"Procedencia : "+i.procedencia)
        pdf.drawString(280,y , u"Destino : "+i.destino)
        pdf.drawString(400,y , u"Placa Vehículo : "+i.placa_vehiculo)
        y -= baja
        pdf.drawString(30,y , u"Días Estadia : "+str(i.dias_estadia))
        pdf.drawString(180,y , u"No. Adultos : "+str(i.no_adultos))
        pdf.drawString(250,y , u"No. Niños : "+str(i.no_ninos))
        pdf.drawString(400,y , u"Equipaje : "+i.equipaje)
        y -= baja
        pdf.drawString(30,y , u"Recibo Caja : "+i.no_recibo_caja)
        pdf.drawString(180,y , u"Consecutivo : "+i.consecutivo)
        pdf.drawString(350,y , u"Empresa : "+i.empresa)
        y -= baja
        pdf.line(30,y,x,y)
        y -= baja
        if y<=30:
            pdf.showPage()
            y= 680    
                      
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionRegistroXlsView(request):
    #idrecibos = request.session['lista_id_filtro_recibo_caja']
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    #recibos_detalle = ReciboCajaDetalle.objects.filter(id=idsesionempaque)
    'IdHabitacion','IdTercero','check_in','hora_check_in','check_out','hora_check_out','no_de_noches','valor_pago','pagado'
    'consecutivo','descripcion','tarifa_habitacion','ocupacion','empresa','motivo_viaje','procedencia','destino','placa_vehiculo','dias_estadia',
    'no_adultos','no_niños','equipaje','pagado','no_recibo_caja'
    
    worksheet.write('A1','Habitación' )
    worksheet.write('B1','Tercero' )
    worksheet.write('C1','Check In')
    worksheet.write('D1','Hora Check In')
    worksheet.write('D1','Check Out')
    worksheet.write('F1','Hora Check Out')
    worksheet.write('G1','no_de_noches')
    worksheet.write('H1','Valor Pago')
    worksheet.write('L1','Pagado')
    worksheet.write('J1','Descripción')
    worksheet.write('K1','Tarifa Habitación')
    worksheet.write('L1','Recibo Caja')
    worksheet.write('M1','Consecutivo')
    worksheet.write('N1','Empresa')
    worksheet.write('O1','Motivo Viaje')
    worksheet.write('P1','Procedencia')
    worksheet.write('Q1','Destino')
    worksheet.write('R1','Placa Vehículo')
    worksheet.write('S1','Días Estadia')
    worksheet.write('T1','No. Adultos')
    worksheet.write('U1','No. Niños')
    worksheet.write('V1','Equipaje')
    worksheet.write('W1','Pagado')
    worksheet.write('X1','Recibo Caja')
    
    id_registros = request.session['lista_id_filtro_registros_hotel']
    n = 2
    if request.session['lista_id_filtro_registros_hotel']:
        id_reservas = request.session['lista_id_filtro_registros_hotel']
        registros = RegistroHotel.objects.filter(id__in=id_registros)
    else:
        registros = RegistroHotel.objects.all()    
    for j in registros: 
        nn = str(n)
        habitacion = j.IdHabitacion.descripcion
        check_in = j.check_in.strftime("%d/%m/%Y")
        hora_check_in = j.hora_check_in.strftime("%H:%M:%S")
        if j.check_out == None:
            check_out =''
            hora_check_out =''
        else:    
            check_out = j.check_out.strftime("%d/%m/%Y")
            hora_check_out = j.hora_check_out.strftime("%H:%M:%S")
        
        if j.IdTercero.razon_social=='' :
            tercero = j.IdTercero.apenom
        else:
            tercero = j.IdTercero.razon_social
        if j.pagado == True:
            pagado = 'Si'       
        else:         
            pagado = 'No'
        exec("worksheet.write('A"+nn+"','"+habitacion+"' )")
        exec("worksheet.write('B"+nn+"','"+tercero+"' )")
        exec("worksheet.write('C"+nn+"','"+check_in+"' )")
        exec("worksheet.write('D"+nn+"','"+hora_check_in+"' )")
        exec("worksheet.write('E"+nn+"','"+check_out+"' )")
        exec("worksheet.write('F"+nn+"','"+hora_check_out+"' )")
        exec("worksheet.write('G"+nn+"','"+str(j.no_de_noches)+"' )")
        exec("worksheet.write('H"+nn+"','"+str(j.valor_pago)+"' )")
        exec("worksheet.write('I"+nn+"','"+pagado+"' )")
        exec("worksheet.write('J"+nn+"','"+j.descripcion+"' )")
        exec("worksheet.write('K"+nn+"','"+str(j.tarifa_habitacion)+"' )")
        exec("worksheet.write('L"+nn+"','"+j.no_recibo_caja+"' )")
        exec("worksheet.write('M"+nn+"','"+j.consecutivo+"' )")
        exec("worksheet.write('N"+nn+"','"+j.empresa+"' )")
        exec("worksheet.write('O"+nn+"','"+j.motivo_viaje+"' )")
        exec("worksheet.write('P"+nn+"','"+j.procedencia+"' )")
        exec("worksheet.write('Q"+nn+"','"+j.destino+"' )")
        exec("worksheet.write('R"+nn+"','"+j.placa_vehiculo+"' )")
        exec("worksheet.write('S"+nn+"','"+str(j.dias_estadia)+"' )")
        exec("worksheet.write('T"+nn+"','"+str(j.no_adultos)+"' )")
        exec("worksheet.write('U"+nn+"','"+str(j.no_ninos)+"' )")
        exec("worksheet.write('V"+nn+"','"+j.equipaje+"' )")
        exec("worksheet.write('W"+nn+"','"+pagado+"' )")
        exec("worksheet.write('X"+nn+"','"+j.no_recibo_caja+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'registros.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    

############################### IMPRESION EN UNA IMPRESORA LOCAL

""" Hola Fernando.

Mi ideal al respecto es usar python-poppler-qt4.

Lamentablemente al ser un binding bastante chico e independiente de
PyQt4 (si un día Qt incorpora Poppler de forma que termine siendo
soportado directamente por PyQt y PySide bailo en una pata) siempre tuvo
varias personas manteniendo copias independientes (entre ellas Roberto
Alsina). Pero hace un tiempo un flaco tomó la posta de mantenerlo más
seriamente (no digo que lo haya cumplido):

http://code.google.com/p/python-poppler-qt4/

En cuanto al soporte Windows, hay por lo menos un instalador para Windows:

https://home.in.tum.de/~lorenzph/python-poppler-qt4/

A continuación mi código para imprimir. Tengo hecho también un form de
vista en pantalla, si te sirve te lo paso.

from PyQt4 import QtGui
try:
import QtPoppler
except ImportError:
try:
import popplerqt4 # Nombre alternativo del módulo
QtPoppler = popplerqt4
except ImportError:
pass


def printpdf(reportfile,printer):

#dpi=printer.resolution()
#print dpi
#if dpi>300:
dpi=300
printer.setResolution(300)

doc = QtPoppler.Poppler.Document.load(reportfile)
painter = QtGui.QPainter()
painter.begin(printer)
progress=QtGui.QProgressDialog (u"Imprimiendo...", u"Cancelar",
0, doc.numPages())
progress.open()
try:
for i in range(0,doc.numPages()):
if i>0: printer.newPage()
page = doc.page(i)
painter.drawImage(0, 0, page.renderToImage(dpi,dpi))
del page
progress.setValue(i)

painter.end()
except:
printer.abort()
raise

printer = QtGui.QPrinter()
filename = tempfile.mkstemp(suffix='.pdf', prefix='report')[1]
report.generate_by(PDFGenerator, filename=filename)
printpdf(filename, printer) """