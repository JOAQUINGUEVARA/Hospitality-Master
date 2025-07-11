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
from django.contrib.auth.models import User

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
import json
from datetime import datetime
import math

from .forms import RecetaForm,RecetaIngredienteForm,OdenProduccionForm
from .models import Receta,RecetaIngrediente,OrdenProduccion,Ingrediente,TipoDocumentoCocina,OrdenProduccionIngrediente
from .filters import RecetaFilter,IngredienteFilter,OrdenProduccionFilter
from .tables import RecetaTable,RecetaIngredienteTable,IngredienteTable,OrdenProduccionTable,OrdenProduccionIngredienteTable
from core.models import Empresa
from inventarios.models import MaestroItem,AcumuladoItem
from inventarios import views as InventariosViews

from django.db import transaction

# Create your views here.

class MenuCocina(TemplateView):
    template_name = "cocina/menu_cocina.html"

class MenuProcesosCocinaView(TemplateView):
    template_name = "cocina/menu_procesos_cocina.html"
    
def IngredienteListView(request):
    queryset = Ingrediente.objects.all()
    f =  IngredienteFilter (request.GET, queryset=queryset)
    ingredientes = IngredienteTable(f.qs)
    ingredientes.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'ingredientes':ingredientes,'filter':f}
    return render(request, 'cocina/ingredientes_lista.html', context) 

def RecetaListView(request):
    queryset = Receta.objects.all()
    f =  RecetaFilter (request.GET, queryset=queryset)
    recetas = RecetaTable(f.qs)
    request.session['filtro_recetas'] = False
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
    request.session['filtro_recetas'] = lista_id    
    recetas.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'recetas':recetas,'filter':f}
    return render(request, 'cocina/recetas_lista.html', context) 

def RecetaIngredientesListView(request,id):
    idreceta = id
    receta = RecetaTable(Receta.objects.filter(id=id))
    queryset = RecetaIngrediente.objects.filter(receta_id=id)
    receta_ingrediente = RecetaIngredienteTable(queryset)
    context = {'receta':receta,'receta_ingrediente':receta_ingrediente,'idreceta':idreceta}
    return render(request, 'cocina/receta_ingredientes_lista.html', context) 

class CreaRecetaView(LoginRequiredMixin,CreateView):
    model = Receta
    template_name = 'cocina/receta_form.html'
    form_class = RecetaForm
    
    def get_success_url(self):
        idreceta = self.object.id
        self.request.session['idreceta' ] = idreceta
        return redirect('recetas_list',idreceta)   

    def form_valid(self, form):
        iditem = self.request.session['idproducto' ]
        if form.is_valid():
            receta = form.save(commit=False)
            receta.producto_id = iditem
            receta.save()
            return redirect('recetas_lista')

class CreaIngredienteRecetaView(LoginRequiredMixin,CreateView):
    model = RecetaIngrediente
    template_name = 'cocina/ingrediente_receta_form.html'
    form_class = RecetaIngredienteForm
    
    def get_success_url(self):
        idreceta = self.object.id
        self.request.session['idreceta' ] = idreceta
        return redirect('receta_ingredientes_list',idreceta)   

    def form_valid(self, form):
        idreceta = self.request.session['idreceta' ]
        if form.is_valid():
            receta_ingrediente = form.save(commit=False)
            receta_ingrediente.receta_id = idreceta
            receta_ingrediente.save()
            return redirect('receta_ingredientes_lista',idreceta)        

def RecetaIngredienteView(request,id):
    receta_ingrediente = RecetaIngrediente.objects.filter(receta_id=id)
    if not receta_ingrediente:
        mensaje1 = "No hay ingredientes creados para esta Receta"
        mensaje2 = ""
        mensaje3 = ""
        parametro = id  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'cocina/mensaje_receta_ingredientes.html', context)
    
    receta_ingrediente = RecetaIngredienteTable(receta_ingrediente)
    receta_ingrediente.paginate(page=request.GET.get("page", 1), per_page=12)
    
    context = {'receta_ingrediente':receta_ingrediente}
    return render(request, 'cocina/receta_ingredientes_lista.html', context)

class EditaIngredienteRecetaView(LoginRequiredMixin,UpdateView):
    model = RecetaIngrediente
    fields = ['ingrediente','cantidad_necesaria']
    template_name = 'cocina/ingrediente_receta_form.html'
    success_url = reverse_lazy('recetas_lista')    

class BorraRecetaView(LoginRequiredMixin,DeleteView):
    model = Receta
    success_url = reverse_lazy('recetas_lista')
    template_name = 'cocina/confirma_borrado.html' 
    success_message = model._meta.verbose_name + "RegistroHotel Borrado"
    
class BorraIngredienteRecetaView(LoginRequiredMixin,DeleteView):
    model = RecetaIngrediente
    #success_url = reverse_lazy('receta_ingredientes_lista')
    template_name = 'cocina/confirma_borrado.html' 
    success_message = model._meta.verbose_name + "ingrediente Borrado"   

    def get_success_url(self, **kwargs) -> str:
        pk = self.kwargs['pk']
        return reverse_lazy('receta_ingredientes_lista', kwargs={'id': pk})
    
def FiltrarItemInventarioMateriaPrimaView(request):
    tipo_item = request.GET.get('tipo_item', None)
    items_inventario = MaestroItem.objects.filter(tipo_producto=tipo_item).values('descripcion', 'id')
    return HttpResponse(json.dumps( list(items_inventario)), content_type='application/json')

def GuardaIdProducto(request):
    idProducto = request.GET.get('id', None)
    request.session['idproducto'] = idProducto
    data = {'id':idProducto}
    return JsonResponse(data)

def GuardaIdIngredienteReceta(request):
    idingrediente = request.GET.get('idingrediente', None)
    request.session['idingrediente_receta'] = idingrediente
    data={'id':idingrediente}
    return JsonResponse(data)   

def GuardaIdReceta(request):
    idreceta = request.GET.get('idreceta', None)
    request.session['idreceta'] = idreceta
    data={'id':idreceta}
    return JsonResponse(data)    

def GuardaIdOrdenProduccion(request):
    idorden = request.GET.get('idorden', None)
    request.session['orden_produccion_id'] = idorden
    data={'id':idorden}
    return JsonResponse(data)  

def OrdenProduccionListView(request):
    queryset = OrdenProduccion.objects.all()
    f =  OrdenProduccionFilter (request.GET, queryset=queryset)
    ordenes = OrdenProduccionTable(f.qs)
    request.session['filtro_id_ordenes_produccion'] = False
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
    request.session['filtro_id_ordenes_produccion'] = lista_id    
    ordenes.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'ordenes':ordenes,'filter':f}
    return render(request, 'cocina/ordenes_produccion_lista.html', context) 

def OrdenProduccionDetalleView(request,id):
    #id = request.session['idorden_produccion'] 
    print('Id',id)
    orden = OrdenProduccionTable(OrdenProduccion.objects.filter(id=id))
    ingredientes = OrdenProduccionIngredienteTable(OrdenProduccionIngrediente.objects.filter(orden_id=id))
    context = {'orden':orden,'ingredientes':ingredientes}
    #context = {'orden':orden}
    return render(request, 'cocina/orden_produccion_ingrediente_lista.html', context) 

class CreaOrdenProduccionView(LoginRequiredMixin,CreateView):
    model = OrdenProduccion
    template_name = 'cocina/orden_produccion_form.html'
    form_class = OdenProduccionForm
    
    def get_success_url(self):
        idorden = self.object.id
        self.request.session['idorden' ] = idorden
        return redirect('ordenes_produccion_lista',idorden)   

    def form_valid(self, form):
        #iditem = self.request.session['idproducto' ]
        if form.is_valid():
            tipodocumento = TipoDocumentoCocina.objects.get(idTipo='01')
            anumero = tipodocumento.actual +1
            snumero = str(anumero).zfill(tipodocumento.longitud)
            snumero = (tipodocumento.caracteres).strip()+snumero
            orden = form.save(commit=False)
            orden.IdUsuario_id = self.request.user.id
            orden.numero = snumero
            orden.estado = 'Pendiente'
            orden.save()
            TipoDocumentoCocina.objects.filter(idTipo='01').update(actual = anumero)
            return redirect('ordenes_produccion_lista')

def ValidaCreaIngredientesOrdenProduccionView(request):
    orden_id = request.session['orden_produccion_id']
    #orden = OrdenProduccion.objects.get(id=orden_id)
    if OrdenProduccionIngrediente.objects.filter(orden_id=id).exists():
       mensaje1="Esta Orden ya tiene ingredientes."
       mensaje2 = 'Adicione ingredientes adicionales con el botón Ad.Item'
       mensaje3 = ''
       parametro = 1
       return render(request,'cocina/mensaje_orden_produccion.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'parametro':parametro}) 
    else:    
        return redirect('orden_produccion_detalle',id)
    

class BorraOrdenProduccionView(LoginRequiredMixin,DeleteView):
    model = Receta
    success_url = reverse_lazy('recetas_list')
    template_name = 'inventarios/confirma_borrado.html' 
    success_message = model._meta.verbose_name + "RegistroHotel Borrado"

def ValidaBorraOrdenProduccionView(request,id):
    request.session['orden_produccion_id'] = id
    orden_produccion =OrdenProduccion.objects.get(id=id)
    if  orden_produccion.estado == 'Producido':
        mensaje1="Esta Orden ya se ejecutó, no puede ser eliminada."
        mensaje2 = ''
        mensaje3 = ''
        parametro = 1
        return render(request,'cocina/mensaje_orden_produccion.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'parametro':parametro})
    else:
        if OrdenProduccionIngrediente.objects.filter(orden_id=id).exists():
            mensaje1="Esta Orden ya tiene ingrediente asignados,"
            mensaje2 = 'Para Borrarla. Debe eliminar los ingredientes.'
            return render(request,'cocina/mensaje_orden_produccion.html',{'mensaje1':mensaje1,'mensaje2':mensaje2})
        
def ValidaBorradoIngredienteOrdenProduccionView(request,id):
    request.session['item_orden_produccion_id'] = id
    orden_ingrediente = OrdenProduccionIngrediente.objects.get(id=id)
    orden_produccion =OrdenProduccion.objects.get(id=orden_ingrediente.orden_id)
    if  orden_produccion.estado == 'Producido':
        mensaje1="Esta Orden ya se ejecutó, no puede ser modificada."
        mensaje2 = ''
        mensaje3 = ''
        parametro = 2
        return render(request,'cocina/mensaje_orden_produccion.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'parametro':parametro,'id':orden_produccion.id})
    else:
        OrdenProduccionIngrediente.objects.filter(id=id).delete()
        return redirect('orden_produccion_detalle',orden_produccion.id)

def ValidaEditaOrdenProduccionView(request,id):
    request.session['orden_produccion_id'] = id 
    orden_produccion =OrdenProduccion.objects.get(id=id)
    if  orden_produccion.estado == 'Producido':
        mensaje1="Esta Orden ya se ejecutó, no puede ser modificada."
        mensaje2 = ''
        mensaje3 = ''
        parametro = 1
        return render(request,'cocina/mensaje_orden_produccion.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'parametro':parametro})
    else:
        """ if OrdenProduccionIngrediente.objects.filter(orden_id=id).exists():
            mensaje1="Esta Orden ya tiene ingrediente asignados,"
            mensaje2 = 'Debe eliminarlos y volver a cargarlos con la nueva información de la orden. '
            mensaje3 = ''
            parametro = 1
            return render(request,'cocina/mensaje_orden_produccion.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'parametro':parametro}) """
        return redirect('edita_orden_produccion',id)

class EditaOrdenProduccionView(LoginRequiredMixin,UpdateView):
    model = OrdenProduccion
    fields = ['receta','cantidad_producir']
    template_name = 'cocina/orden_produccion_form.html'
    success_url = reverse_lazy('ordenes_produccion_lista')          

def ValidaCargaItemsOrdenProduccionView(request,id):
    request.session['orden_produccion_id'] = id
    orden_produccion = OrdenProduccion.objects.get(id=id)
    if OrdenProduccionIngrediente.objects.filter(orden_id=id).exists():
        mensaje1="Esta Orden ya tiene ingrediente asignados."
        mensaje2 = ''
        mensaje3 = ''
        parametro = 1
        return render(request,'cocina/mensaje_orden_produccion.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'parametro':parametro})
    else:
        return redirect('carga_items_orden_produccion',id)
    
def CargaItemsOrdenProduccionView(request,id):
    orden_produccion = OrdenProduccion.objects.get(id=id)
    idreceta = orden_produccion.receta_id 
    ingrediente_receta = RecetaIngrediente.objects.filter(receta_id=idreceta)
    orden_ingrediente = OrdenProduccionIngrediente()
    for i in ingrediente_receta:
        orden_ingrediente.ingrediente_id=i.ingrediente_id
        orden_ingrediente.cantidad_necesaria=i.cantidad_necesaria
        acumulado_inv = AcumuladoItem.objects.get(IdItem_id=i.ingrediente.ingrediente_id)
        saldo = acumulado_inv.if_12
        item = MaestroItem.objects.get(id=i.ingrediente.ingrediente_id)
        orden_ingrediente.cantidad_stock = saldo
        cantidad_necesaria = i.cantidad_necesaria * orden_produccion.cantidad_producir
        orden_ingrediente.cantidad_necesaria = cantidad_necesaria
        cantidad_compra = cantidad_necesaria - saldo 
        if cantidad_compra<0:
            cantidad_compra = 0
        orden_ingrediente.cantidad_a_comprar = cantidad_compra
        orden_ingrediente.precio_compra_unitario = item.costo_prom
        orden_ingrediente.orden_id = id
        orden_ingrediente.save()
        orden_ingrediente.id += 1 
    return redirect('orden_produccion_detalle',id)

def EjecutaOrdenProduccionView(request,id):
    orden_produccion = OrdenProduccion.objects.get(id=id)
    idreceta = orden_produccion.receta_id 
    ingrediente_receta = RecetaIngrediente.objects.filter(receta_id=idreceta)
    orden_ingrediente = OrdenProduccionIngrediente()
    fecha = orden_produccion.fecha
    year = orden_produccion.fecha
    anio = year.year
    mes = year.month
    tipo='09'
    detalle=''
    idusuario = request.user.id
    #InventariosViews.CreaDocumentoSalidaInventariosCabeza(fecha,tipo,anio,mes,orden_produccion.numero,'',detalle,idusuario)
    costo_orden = 0
    for i in ingrediente_receta:
        acumulado_inv = AcumuladoItem.objects.get(IdItem_id=i.ingrediente.ingrediente_id)
        saldo = acumulado_inv.if_12
        print(acumulado_inv,' Saldo',saldo)
        item = MaestroItem.objects.get(id=i.ingrediente.ingrediente_id)
        cantidad_necesaria = i.cantidad_necesaria * orden_produccion.cantidad_producir
        orden_ingrediente.cantidad_necesaria = cantidad_necesaria
        cantidad_compra = cantidad_necesaria - saldo
        costo_compra = cantidad_compra * item.costo_prom
        OrdenProduccionIngrediente.objects.filter(orden_id=id,ingrediente_id=i.ingrediente_id).update(cantidad_necesaria=cantidad_necesaria,cantidad_stock=saldo,cantidad_a_comprar=cantidad_compra,costo_compra=costo_compra,precio_compra_unitario=item.costo_prom)
        if cantidad_compra<0:
            cantidad_compra = 0
        costo_orden = cantidad_necesaria * item.costo_prom
        #InventariosViews.CreaDocumentoSalidaInventariosCuerpo(tipo,anio,mes,orden_produccion.numero,'',item.id,cantidad_necesaria,0,0)
        OrdenProduccion.objects.filter(id=id).update(costo_orden=costo_orden) 
    return redirect('orden_produccion_detalle',id)

def AplicaOrdenProduccionView(request,id):
    orden_produccion = OrdenProduccion.objects.get(id=id)
    idreceta = orden_produccion.receta_id 
    ingrediente_receta = RecetaIngrediente.objects.filter(receta_id=idreceta)
    orden_ingrediente = OrdenProduccionIngrediente()
    fecha = orden_produccion.fecha
    year = orden_produccion.fecha
    anio = year.year
    mes = year.month
    tipo='09'
    detalle=''
    idusuario = request.user.id
    InventariosViews.CreaDocumentoSalidaInventariosCabeza(fecha,tipo,anio,mes,orden_produccion.numero,'',detalle,idusuario)
    for i in ingrediente_receta:
        acumulado_inv = AcumuladoItem.objects.get(IdItem_id=i.ingrediente.ingrediente_id)
        saldo = acumulado_inv.if_12
        item = MaestroItem.objects.get(id=i.ingrediente.ingrediente_id)
        cantidad_necesaria = i.cantidad_necesaria * orden_produccion.cantidad_producir
        orden_ingrediente.cantidad_necesaria = cantidad_necesaria
        cantidad_compra = cantidad_necesaria - saldo 
        if cantidad_compra<0:
            cantidad_compra = 0
        InventariosViews.CreaDocumentoSalidaInventariosCuerpo(tipo,anio,mes,orden_produccion.numero,'',item.id,cantidad_necesaria,0,0)
        OrdenProduccion.objects.filter(id=id).update(estado='Producido') 
    return redirect('orden_produccion_detalle',id)

def elaborar_orden_produccion(orden_id):
    from .models import OrdenProduccion, RecetaIngrediente, Ingrediente, MaestroItem

    with transaction.atomic():
        orden = OrdenProduccion.objects.select_related('receta').get(id=orden_id)
        receta_ingredientes = RecetaIngrediente.objects.filter(receta=orden.receta)
        for ri in receta_ingredientes:
            cantidad_total = ri.cantidad_necesaria * orden.cantidad_producir
            ingrediente = ri.ingrediente
            # Aquí deberías tener un modelo de inventario para descontar el stock
            # Por ejemplo:
            # inventario = Inventario.objects.get(item=ingrediente.ingrediente)
            # if inventario.cantidad < cantidad_total:
            #     raise Exception(f"No hay suficiente stock de {ingrediente.descripcion}")
            # inventario.cantidad -= cantidad_total
            # inventario.save()
        orden.estado = 'producido'
        orden.save()

def PoneIngredienteView(request):
    items = MaestroItem.objects.filter(tipo_producto='MP')
    for j in items:
        if not Ingrediente.objects.filter(ingrediente_id=j.id).exists():
            ingrediente = Ingrediente()
            ingrediente.ingrediente_id = j.id
            ingrediente.descripcion = j.descripcion
            ingrediente.unidad_medida_id = j.IdUnidadMedida_id
            ingrediente.save()
    mensaje1 = "Proceso Terminado"
    mensaje2 = ""
    mensaje3 = ""
    parametro = '' 
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
    return render(request, 'cocina/mensaje_fin_proceso.html', context)


#################################################### Impresiones ###################################
def ImpresionRecetasXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1','Receta:' )
    worksheet.write('B1','Descripción' )
    if request.session['filtro_recetas']:
        lista_id = request.session['filtro_recetas']
        recetas = Receta.objects.filter(id__in=lista_id).order_by('producto__descripcion')
    else:    
        recetas = Receta.objects.all().order_by('producto__descripcion')
    n=2
    for j in recetas:     
        nn = str(n)
        descripcion = j.producto.descripcion
        exec("worksheet.write('A"+nn+"','Receta:"+descripcion+"' )")
        ingrediente = RecetaIngrediente.objects.filter(receta_id=j.id)
        n = n + 1
        tw = 0
        for i in ingrediente:
            nn = str(n)
            descripcion = i.ingrediente.descripcion
            print(descripcion)
            if tw == 0:
                exec("worksheet.write('A"+nn+"','Ingredientes' )")
                tw = 1
            n = n + 1
            nn = str(n)
            exec("worksheet.write('B"+nn+"','"+descripcion+"' )")
            exec("worksheet.write('C"+nn+"','"+str(i.cantidad_necesaria)+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'recetas.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename        
    return response

def ImpresionRecetasView(request):
    if request.session['filtro_recetas']:
        lista_id = request.session['filtro_recetas']
        recetas = Receta.objects.filter(id__in=lista_id).order_by('producto__descripcion')
    else:    
        recetas = Receta.objects.all().order_by('producto__descripcion')
    #ingredientes = Ingrediente.objects.all().order_by('descripcion')
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
    pdf.drawString(200, y, u"RECETAS/INGREDIENTES")
    pdf.setFont("Helvetica", 9)
    y -= 30
    encabezados = ('Ingrediente', 'Cantidad Nec.','Unidad Med.')
    n = 0
    for receta in recetas:
        y -= 10
        pdf.drawString(30, y, u"RECETA: "+receta.producto.descripcion)
        y -= 20
        ingrediente = RecetaIngrediente.objects.filter(receta_id=receta.id)
        registros = RecetaIngrediente.objects.filter(receta_id=receta.id).count()
        detalle = [(ingrediente.ingrediente.descripcion,ingrediente.cantidad_necesaria,ingrediente.ingrediente.unidad_medida) for ingrediente in ingrediente]
        detalle_ingredientes = Table([encabezados] + detalle, colWidths=[6 * cm,3 * cm,3 * cm,3 * cm])
        detalle_ingredientes.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1),10),
        ]
        ))
        y = y - registros*(25-2*n)
        if y<= 35:
            pdf.showPage()
            y= 700
        detalle_ingredientes.wrapOn(pdf, 300, 800)
        detalle_ingredientes.drawOn(pdf, 30,y)
        y -= 10
        n += 1
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

""" def ImpresionRecetasXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
        
    worksheet.write('A1','Receta:' )
    worksheet.write('B1','Descripción' )
    recetas = Receta.objects.all()
    n=2
    for j in recetas:     
        nn = str(n)
        descripcion = j.producto.descripcion
        exec("worksheet.write('A"+nn+"','Receta:"+descripcion+"' )")
        ingrediente = RecetaIngrediente.objects.filter(receta_id=j.id)
        for i in ingrediente:
            descripcion = i.ingrediente.descripcion
            exec("worksheet.write('A"+nn+"','"+descripcion+"' )")
            exec("worksheet.write('B"+nn+"','"+str(i.cantidad_necesaria)+"' )")
            n += 1
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'receta_ingrediente.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response         """

def ImpresionOrdenesProduccionXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    if request.session['filtro_id_ordenes_produccion']:
        lista_id = request.session['filtro_id_ordenes_produccion']
        ordenes = OrdenProduccion.objects.filter(id__in=lista_id).order_by('-numero')
    else:    
        ordenes = OrdenProduccion.objects.all().order_by('-numero')
    n=2
    sw = 0
    for j in ordenes:     
        nn = str(n)
        exec("worksheet.write('A"+nn+"','Numero' )")
        exec("worksheet.write('B"+nn+"','Fecha' )")
        exec("worksheet.write('C"+nn+"','Receta' )")
        exec("worksheet.write('D"+nn+"','Cantidad Produc.' )")
        exec("worksheet.write('E"+nn+"','Estado' )")
        exec("worksheet.write('F"+nn+"','Costo Orden' )")  
        n += 1    
        nn = str(n)
        desc_receta = j.receta.producto.descripcion
        exec("worksheet.write('A"+nn+"','"+j.numero+"' )")
        exec("worksheet.write('B"+nn+"','"+j.fecha.strftime('%d/%m/%Y')+"' )")
        exec("worksheet.write('C"+nn+"','"+desc_receta+"')")
        exec("worksheet.write('D"+nn+"','"+str(j.cantidad_producir)+"' )")
        exec("worksheet.write('E"+nn+"','"+j.estado+"' )")
        exec("worksheet.write('F"+nn+"','"+str(j.costo_orden)+"' )")     
        n += 1
        nn = str(n)
        exec("worksheet.write('A"+nn+"','Ingrediete' )")
        exec("worksheet.write('B"+nn+"','Cantidad Necesaria' )")
        exec("worksheet.write('C"+nn+"','Stock' )")
        exec("worksheet.write('D"+nn+"','Cantidad a Comprar' )")
        exec("worksheet.write('E"+nn+"','Precio Compra Unitario' )")
        exec("worksheet.write('F"+nn+"','Costo Compra' )")
        n += 1
        ingredientes = OrdenProduccionIngrediente.objects.filter(orden_id=j.id)
        for t in ingredientes:
            nn = str(n)
            ingrediente = Ingrediente.objects.get(id=t.ingrediente_id)
            item = MaestroItem.objects.get(id=ingrediente.ingrediente_id)
            ingr_desc = item.descripcion
            exec("worksheet.write('A"+nn+"','"+ingr_desc+"' )")
            exec("worksheet.write('B"+nn+"','"+str(t.cantidad_necesaria)+"' )")
            exec("worksheet.write('C"+nn+"','"+str(t.cantidad_stock)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(t.cantidad_a_comprar)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(t.precio_compra_unitario)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(t.costo_compra)+"' )") 
            n += 1      
    workbook.close()
    output.seek(0)
    filename = 'orden_produccion.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename        
    return response

def ImpresionOrdenesProduccionView(request):
    if request.session['filtro_id_ordenes_produccion']:
        lista_id = request.session['filtro_id_ordenes_produccion']
        ordenes = OrdenProduccion.objects.filter(id__in=lista_id).order_by('-numero')
    else:    
        ordenes = OrdenProduccion.objects.all().order_by('-numero')
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
    pdf.drawString(200, y, u"ORDEN PRODUCCION")
    pdf.setFont("Helvetica", 9)
    y -= 20
    sw = 0
    for orden in ordenes:
        encabezados = ('numero','Fecha','Receta','Cantidad Produc.','Estado','Costo Orden')
        detalle = [(orden.numero,orden.fecha.strftime('%d/%m/%Y'),orden.receta.producto.descripcion[0:30],'{:,}'.format(orden.cantidad_producir),orden.estado,'{:,}'.format(orden.costo_orden))]
        orden_table = Table([encabezados] + detalle, colWidths=[3 * cm,2 * cm,5 * cm,3 * cm,3 * cm,3 * cm,3 * cm])
        orden_table.setStyle(TableStyle(
        [
        #La primera fila(encabezados) va a estar centrada
        ('ALIGN',(0,0),(3,0),'CENTER'),
        #Los bordes de todas las celdas serán de color negro y con un grosor de 1
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        #El tamaño de las letras de cada una de las celdas será de 10
        ('FONTSIZE', (0, 0), (-1, -1),10),
        ]
        ))
        y = y - 50
        if y<= 35:
            pdf.showPage()
            y= 700
        orden_table.wrapOn(pdf, 300, 800)
        orden_table.drawOn(pdf, 30,y)
        if sw == 0:
           y -= 15
        sw=1   
        ingredientes = OrdenProduccionIngrediente.objects.filter(orden_id=orden.id)
        registros = OrdenProduccionIngrediente.objects.filter(orden_id=orden.id).count()
        encabezados = ("Ingrediente","Cant. Nec.","Stock","Cant.Comprar","Prec.Comp.Unit","Costo Compra")
        detalle = [(ing.ingrediente.descripcion[0:45],'{:,}'.format(ing.cantidad_necesaria),'{:,}'.format(ing.cantidad_stock),'{:,}'.format(ing.cantidad_a_comprar),'{:,}'.format(ing.precio_compra_unitario),'{:,}'.format(ing.costo_compra)) for ing in ingredientes]
        ingredientes = Table([encabezados] + detalle, colWidths=[5 * cm,2 * cm,3 * cm,3 * cm,3 * cm,3 * cm,3 * cm])
        ingredientes.setStyle(TableStyle(
        [
        #La primera fila(encabezados) va a estar centrada
        ('ALIGN',(0,0),(3,0),'CENTER'),
        #Los bordes de todas las celdas serán de color negro y con un grosor de 1
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        #El tamaño de las letras de cada una de las celdas será de 10
        ('FONTSIZE', (0, 0), (-1, -1),10),
        ]
        ))
        b= 0
        y = y - registros*22
        if y<= 35:
            pdf.showPage()
            y= 700
        ingredientes.wrapOn(pdf, 300, 800)
        ingredientes.drawOn(pdf, 30,y)
        y -= 0
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

