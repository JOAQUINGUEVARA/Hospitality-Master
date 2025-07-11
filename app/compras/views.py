from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.urls import reverse_lazy

from django.views.decorators.csrf import csrf_exempt
import re
from django.db.models import Q,Sum

from django.http import HttpResponseBadRequest,HttpResponse, HttpRequest, JsonResponse,HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
#from django.contrib.auth.forms import UserCreationForm
from django.core.serializers import serialize
#from datetime import datetime, date, time
from django.utils import timezone
import datetime
from datetime import timedelta,date

from io import BytesIO

import io
from django.http import FileResponse
import csv
from django.db.models import Subquery
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from decimal import Decimal
from django.template.loader import render_to_string
import json
from django.shortcuts import render, redirect
from django.core import serializers
from django.core.serializers import serialize
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import OrdenCompra,OrdenCompraDetalle,TipoDocumentoCompra,Proveedor,Despacho,DetalleDespacho,ProveedorItem,EmpaqueItem
from .filters import ProveedoresNombreFilter,ProveedoresFilter,OrdenCompraFilter,DespachoFilter,OrdenCompraFilter1,ProveedorItemFilter
from .tables import OrdenCompraTable,OrdenCompraDetalleTable,ProveedoresTable1,ProveedoresTable2,ProveedoresListaTable,ItemsOrdenListaTable,DespachoTable,ProveedorItemTable
from .tables import DespachoDetalleTable,OrdenCompraListaTable,EmpaqueItemTable
from .forms import ProveedoresForm,OrdenCompraForm,ProveedorOrdenCompraForm,DespachoForm,DetalleDespachoForm,ItemEmpaqueForm
from inventarios.tables import ItemsListaTable
from inventarios.models import MaestroItem,Bodega,TipoDocumentoInv,Entrada,EntradaDetalle,Medida
from inventarios.filters import MaestroItemsFilter
from inventarios import views as InventariosViews
from core.models import ValorDefecto,Sucursal,Pais,Departamento,Ciudad,Empresa,Tercero

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

from django.db.models import F, Value, CharField
from django.db.models.functions import Concat

def ProveedoresListView(request):
    queryset = Proveedor.objects.all()
    f =  ProveedoresFilter (request.GET, queryset=queryset)
    proveedores = ProveedoresTable1(f.qs)
    request.session['filtro_proveedores_id'] = False
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
    request.session['filtro_proveedores_id'] = lista_id
    proveedores.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'proveedores':proveedores,'filter':f}
    return render(request, 'compras/proveedores_lista.html', context) 

def DetalleProveedorView(request,id):
    proveedores1 = ProveedoresTable1(Proveedor.objects.filter(id=id))
    proveedores2 = ProveedoresTable2(Proveedor.objects.filter(id=id))
    context = {'proveedores1':proveedores1,'proveedores2':proveedores2}
    return render(request, 'compras/detalle_proveedores_lista.html', context) 


class CreaProveedorView(LoginRequiredMixin,CreateView):
    model = Proveedor
    template_name = 'compras/proveedor_form.html'
    form_class = ProveedoresForm
    
    def get_success_url(self):
        return reverse_lazy('proveedores_list')
    
    def get_initial(self,*args,**kwargs):
        initial=super(CreaProveedorView,self).get_initial(**kwargs)
        valor_defecto_pais = ValorDefecto.objects.get(idValor='02')
        pais = Pais.objects.get(idPais=valor_defecto_pais.valor)
        initial['IdPais'] = pais.id
        valor_defecto_depto = ValorDefecto.objects.get(idValor='03')
        depto = Departamento.objects.get(idDepartamento=valor_defecto_depto.valor)
        initial['departamento'] = depto.id
        valor_defecto_ciudad = ValorDefecto.objects.get(idValor='04')
        ciudad = Ciudad.objects.get(idCiudad=valor_defecto_ciudad.valor)
        initial['ciudad'] = ciudad.id
        return initial
    
    def form_valid(self, form):
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.IdUsuario_id = self.request.user.id
            proveedor.save()
            idproveedor = Proveedor.objects.latest('id')
            proveedor = Proveedor.objects.get(id=idproveedor.id)
            self.request.session['idproveedor' ] = proveedor.id
            Proveedor.objects.filter(id=idproveedor.id).update(apenom = proveedor.apel1.strip()+" "+proveedor.apel2.strip()+" "+proveedor.nombre1.strip()+" "+proveedor.nombre2.strip())
            return redirect('proveedores_list')   


class EditaProveedorView(LoginRequiredMixin,UpdateView):
    model = Proveedor
    fields = ['identificacion','IdTipoIdentificacion','nombre1','nombre2','apel1','apel2','razon_social','IdPais','departamento','ciudad',
                  'direccion','telefono','email','direccion','telefono','email','contacto','por_ica','por_ret_fte']
    template_name = 'compras/proveedor_form.html'
    success_url = reverse_lazy('proveedores_list')

class BorraProveedorView(LoginRequiredMixin,DeleteView):
    model = Proveedor
    success_url = reverse_lazy('proveedores_list')
    template_name = 'core/confirma_borrado.html'

def OrdenesCompraListView(request):
    queryset = OrdenCompra.objects.all().order_by('-fecha','-numero')
    f =  OrdenCompraFilter (request.GET, queryset=queryset)
    ordenes = OrdenCompraTable(f.qs)
    request.session['filtro_idordenes'] = False
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
    request.session['filtro_idordenes'] = lista_id    
    ordenes.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'ordenes':ordenes,'filter':f}
    return render(request, 'compras/ordenes_compra_lista.html', context) 

class CreaOrdenCompraView(LoginRequiredMixin,CreateView):
    model = OrdenCompra
    template_name = 'compras/orden_compra_form.html'
    form_class = OrdenCompraForm

    def get_success_url(self):
        return reverse_lazy('ordenes_compra_list')

    def get_initial(self,*args,**kwargs):
        initial=super(CreaOrdenCompraView,self).get_initial(**kwargs)
        sucursal_defecto = ValorDefecto.objects.get(idValor='01')
        sucursal = Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
        initial['IdSucursal'] = sucursal.id
        #bodega_defecto = ValorDefecto.objects.get(idValor='05')
        #bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
        #initial['IdBodega'] = bodega.id
        idproveedor = self.request.session['idproveedor']
        initial['IdProveedor'] = idproveedor
        initial['fecha'] = date.today()
        return initial
    
    def form_valid(self, form):
        if form.is_valid():
            tipodocumento = TipoDocumentoCompra.objects.get(idTipo='01')
            anumero = tipodocumento.actual +1
            snumero = str(anumero).zfill(tipodocumento.longitud)
            snumero = (tipodocumento.caracteres).strip()+snumero
            compra = form.save(commit=False)
            compra.IdUsuario_id = self.request.user.id
            compra.numero = snumero
            compra.IdTipoDocumento_id = tipodocumento.id
            compra.estado = True
            compra.save()
            TipoDocumentoCompra.objects.filter(idTipo='01').update(actual = anumero)
            return redirect('detalle_orden_compra',compra.id)   

class BuscaProveedorOrdenCompra(SingleTableMixin,FilterView):
    table_class = ProveedoresListaTable
    model = Proveedor
    template_name = "compras/proveedores_orden_compra_filter.html"
    filterset_class = ProveedoresNombreFilter
    paginate_by = 8

class CreaProveedorOrdenCompraView(LoginRequiredMixin,CreateView):
    model = Proveedor
    template_name = 'compras/proveedor_orden_compra_form.html'
    form_class = ProveedorOrdenCompraForm
    
    def get_success_url(self):
        idproveedor = self.object.id 
        ##idproveedor = Proveedor.objects.latest('id')
        proveedor = Proveedor.objects.get(id=idproveedor.id)
        self.request.session['idproveedor' ] = proveedor.id
        return redirect('crea_orden_compra')   

    def get_initial(self,*args,**kwargs):
        #id =self.kwargs['id']
        #self.request.session['tipo_pago'] = id
        initial=super(CreaProveedorOrdenCompraView,self).get_initial(**kwargs)
        valor_defecto_pais = ValorDefecto.objects.get(idValor='02')
        pais = Pais.objects.get(idPais=valor_defecto_pais.valor)
        initial['IdPais'] = pais.id
        valor_defecto_depto = ValorDefecto.objects.get(idValor='03')
        depto = Departamento.objects.get(idDepartamento=valor_defecto_depto.valor)
        initial['departamento'] = depto.id
        valor_defecto_ciudad = ValorDefecto.objects.get(idValor='04')
        ciudad = Ciudad.objects.get(idCiudad=valor_defecto_ciudad.valor)
        initial['ciudad'] = ciudad.id
        #initial['IdTipoProveedor'] = 2
        return initial
    
    def form_valid(self, form):
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.IdUsuario_id = self.request.user.id
            proveedor.save()
            self.request.session['idproveedor' ] = proveedor.id
            Proveedor.objects.filter(id=proveedor.id).update(apenom = proveedor.apel1.strip()+" "+proveedor.apel2.strip()+" "+proveedor.nombre1.strip()+" "+proveedor.nombre2.strip())
            return redirect('crea_orden_compra')   
        
def SeleccionaProveedorOrdenCompra(request):
    idProveedor = request.GET.get('id', None)
    request.session['idproveedor'] = idProveedor
    data = {'id':idProveedor}
    return JsonResponse(data) 
    
def DetalleOrdenCompraView(request,id):
    request.session['idorden']=id
    lista_id = []
    lista_id.append(id)
    request.session['filtro_idordenes'] = lista_id    
    orden = OrdenCompraTable(OrdenCompra.objects.filter(id=id))
    detalle_orden = OrdenCompraDetalleTable(OrdenCompraDetalle.objects.filter(IdOrden_id=id))
    context = {'orden':orden,'detalle_orden':detalle_orden}
    return render(request, 'compras/detalle_orden_compra.html', context) 

def ValidaEditarOrdenCompraDetalleView(request,id):
    request.session['idorden_detalle'] = id 
    orden_detalle = OrdenCompraDetalle.objects.get(id=id)
    orden = OrdenCompra.objects.get(id=orden_detalle.IdOrden_id)
    pk=id
    if (orden.despacho).strip() =='':
        return redirect('edita_orden_compra_detalle',pk)
    else:
        mensaje1="Esta Orden tiene Despacho,"
        mensaje2 = 'No Se Puede Modificar'
        mensaje3 = ''
        return render(request,'compras/mensaje_editar_orden_compra.html',{'mensaje1':mensaje1,'mensaje2':mensaje2})

class EditaOrdenCompraView(LoginRequiredMixin,UpdateView):
    model = OrdenCompra
    fields = ['fecha','IdProveedor','detalle','IdSucursal']
    template_name = 'compras/orden_compra_form.html'
    #success_url = reverse_lazy('ordenes_compra_list')

    def get_success_url(self, *args, **kwargs):
        idorden = self.object.pk
        orden = OrdenCompra.objects.get(id=idorden)
        if Despacho.objects.filter(numero=orden.despacho).exists():
            despacho = Despacho.objects.get(numero=orden.despacho)
            if despacho.IdProveedor_id != orden.IdProveedor_id:
                #if despacho.IdSucursal_id != orden.IdSucursal_id:
                #Despacho.objects.filter(numero=orden.despacho).update(IdSucursal_id=orden.IdSucursal_id)
                Despacho.objects.filter(numero=orden.despacho).update(IdProveedor_id=orden.IdProveedor_id)
        return reverse_lazy('ordenes_compra_list')
        

class EditaOrdenCompraDetalleView(LoginRequiredMixin,UpdateView):
    model = OrdenCompraDetalle
    fields = ['IdItem','cantidad_empaque','cantidad_unidad_empaque','valor_unidad_empaque','cantidad_unidades_compra','valor_compra']
    template_name = 'compras/orden_compra_detalle_form.html'
    id = 1
    #success_url = reverse_lazy('direcciona_inventarios',args=[id])    

    def get_success_url(self, *args, **kwargs):
        #id_orden_detalle = self.object.pk
        id_orden_detalle = self.request.session['id_orden_detalle']
        id_item_anterior = self.request.session['id_item_anterior']
        orden_detalle = OrdenCompraDetalle.objects.get(id=id_orden_detalle)
        orden = OrdenCompra.objects.get(numero=orden_detalle.numero)
        #year = orden.fecha
        #anio = year.year
        #mes = year.month
        #InventariosViews.ReversaAcumuladosEntradaInventarios(id_item_anterior,cantidad_anterior,mes,anio)
        orden_detalle = OrdenCompraDetalle.objects.get(id=id_orden_detalle)
        id_item_actual = orden_detalle.IdItem_id
        detalle = OrdenCompraDetalle.objects.filter(numero=orden_detalle.numero)
        Total = 0
        for i in detalle:
            total = Total + i.valor_compra
        OrdenCompra.objects.filter(numero=orden_detalle.numero).update(valor=total)
        orden_detalle = OrdenCompraDetalle.objects.filter(numero=orden.numero) 
        for g in orden_detalle:
            item = g.IdItem_id
            despacho_detalle = DetalleDespacho.objects.filter(numero=orden.despacho)
            for h in despacho_detalle:
                if h.IdItem_id==item:
                    if h.cantidad_enviada > g.cantidad_unidades:
                        mensaje1="El Despacho quedó con mas unidades despachadas, que las de la Orden de Compra."
                        mensaje2 = ''
                        mensaje3 = ''
                        return render(self.request,'compras/mensaje_editar_orden_compra.html',{'mensaje1':mensaje1,'mensaje2':mensaje2}) 
        return reverse_lazy('detalle_orden_compra', kwargs={'id':orden.id})     

def ConfirmaBorradoOrdenCompraView(request,id):
    request.session['idorden'] = id 
    #orden = OrdenCompra.objects.get(id=id)
    if Despacho.objects.filter(IdOrdenCompra_id=id).exists():
        despacho = Despacho.objects.get(IdOrdenCompra_id=id)
        mensaje1="Esta Orden tiene el Despacho <"+despacho.numero+">"
        mensaje2 = ',No Se Puede Modificar'
        mensaje3 = 'Debe borrar primero el despacho'
        return render(request,'compras/mensaje_borrar_orden_compra.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3})
    else:
        mensaje1="Esta seguro de borrar esta orden"
        mensaje2 = ''
        mensaje3 = ''
        return render(request,'compras/mensaje_confirma_borra_orden_compra.html',{'mensaje1':mensaje1})
            
               
""" class BorraOrdenCompraView(LoginRequiredMixin,DeleteView):
    model = OrdenCompra
    success_url = reverse_lazy('ordenes_compra_list')
    template_name = 'inventarios/confirma_borrado.html' """

def BorraOrdenCompraView(request,id):
    if id == 1:
        id = request.session['idorden']
        OrdenCompraDetalle.objects.filter(IdOrden_id=id).delete()
        OrdenCompra.objects.filter(id=id).delete()
    return redirect('ordenes_compra_list')

def ConfirmaBorradoOrdenCompraDetalleView(request,id):
    request.session['idorden'] = id
    if Despacho.objects.filter(IdOrdenCompra_id=id).exists():
        despacho = Despacho.objects.get(IdOrdenCompra_id=id)
        mensaje1="Esta Orden tiene el Despacho <"+despacho.numero+">"
        mensaje2 = ',No Se Puede Modificar'
        mensaje3 = 'Debe borrar primero el despacho'
        return render(request,'compras/mensaje_borrar_orden_compra.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3})
    else:
        mensaje1="Esta seguro de borrar este registro?"
        mensaje2 = ''
        mensaje3 = ''
        return render(request,'compras/mensaje_confirma_borra_detalle_orden_compra.html',{'mensaje1':mensaje1})
    
def BorraOrdenCompraDetalleView(request,id):
    id_item_anterior = request.session['id_item_anterior']
    id_orden_detalle = request.session['id_orden_detalle']
    cantidad_anterior = request.session['cantidad_anterior']
    numero_orden = request.session['numero_orden']
    orden = OrdenCompra.objects.get(numero=numero_orden)
    year = orden.fecha
    anio = year.year
    mes = year.month
    invinic = False
    if id == 1:
        InventariosViews.ReversaAcumuladosEntradaInventarios(id_item_anterior,cantidad_anterior,mes,anio,invinic)
        OrdenCompraDetalle.objects.filter(id=id_orden_detalle).delete()

    return redirect('detalle_orden_compra', orden.id)

def VerificaDetalleOrdenCompraView(request,id):
    aa = OrdenCompraDetalle.objects.filter(IdOrden_id=id).exists()
    if aa:
        return redirect('detalle_orden_inventario',id)
    else:
        request.session['idorden'] = id
        return redirect('selecciona_item_orden_inventarios',id) 
    
def SeleccionaItemOrdenCompraView(request,id):
    request.session['idorden'] = id
    return redirect(reverse('filtra_item_orden_compra'))    

class FiltraItemOrdenCompraView(SingleTableMixin, FilterView):
    table_class = ItemsOrdenListaTable
    #empaque = EmpaqueItemTable(EmpaqueItem.objects.all())
    model = MaestroItem
    template_name = "compras/items_orden_compra_filter.html"
    filterset_class = MaestroItemsFilter
    paginate_by = 8


def ObtenerUnidadMedidaView(request):
    item_id = request.GET.get('id')
    try:
        item = MaestroItem.objects.get(id=item_id)
        unidad = item.IdUnidadMedida.descripcion  # o .abreviatura si prefieres
        return JsonResponse({'unidad': unidad,'id':item.id})
    except MaestroItem.DoesNotExist:
        return JsonResponse({'unidad': '','id':0})

def GuardaItemOrdenCompra(request):
    #request.session['sel_item']= True
    #a = request.session['sel_item']
    iditem = request.GET.get('id', None)
    cantidad_unidad_empaque = request.GET.get('cantidad_unidad_empaque', None)
    valor_unidad_empaque = request.GET.get('valor_unidad_empaque', None)
    cantidad_empaque = request.GET.get('cantidad_empaque', None)
    cantidad_unidades_compra = request.GET.get('cantidad_unidades_compra', None)
    valor_compra = request.GET.get('valor_compra', None)

    idorden = request.session['idorden']
    AdicionaItemOrdenCompra(iditem,idorden,cantidad_unidad_empaque,valor_unidad_empaque,cantidad_empaque,cantidad_unidades_compra,valor_compra)
    data={'a':0}
    return JsonResponse(data)

def AdicionaItemOrdenCompra(iditem,idorden,cantidad_unidad_empaque,valor_unidad_empaque,cantidad_empaque,cantidad_unidades_compra,valor_compra):
    detalle_orden = OrdenCompraDetalle()
    item = MaestroItem.objects.get(id=iditem)
    orden = OrdenCompra.objects.get(id=idorden)
    idtipodoc = TipoDocumentoCompra.objects.get(idTipo='01')
    detalle_orden.numero = orden.numero
    detalle_orden.IdTipoDocumento_id = idtipodoc.id
    detalle_orden.IdOrden_id = orden.id
    detalle_orden.IdItem_id = iditem
    detalle_orden.estado = 1
    detalle_orden.valor_compra = float(valor_compra)
    if cantidad_empaque == '':
        cantidad_empaque = 1
    detalle_orden.cantidad_empaque = int(cantidad_empaque)
    detalle_orden.cantidad_unidad_empaque =  int(cantidad_unidad_empaque)
    detalle_orden.valor_unidad_empaque =  float(valor_unidad_empaque)
    detalle_orden.cantidad_unidades_compra = int(cantidad_unidades_compra)
    detalle_orden.valor_unitario = float(valor_compra)/int(cantidad_unidades_compra)
    detalle_orden.save()
    #InterfaseSalidaInventariosCuerpo(salida.numero,iditem,cantidad,item.valor_venta,item.valor_venta*int(float(cantidad)))
    orden_detalle_regs = OrdenCompraDetalle.objects.filter(numero=orden.numero)
    total=0
    items = 0
    year = orden.fecha
    anio = year.year
    mes = year.month
    for sal in orden_detalle_regs:
        total = total + sal.valor_compra
        items = items + 1
        #OrdenCompraDetalle.objects.filter(id=sal.id).update(valor_total=sal.valor*sal.cantidad)
        #InventariosViews.ActualizaAcumuladosInventarios(sal.IdItem_id,sal.cantidad,mes,anio,'orden')
        OrdenCompra.objects.filter(numero=orden.numero).update(valor=total)

def ValidaCreaDetalleOrdenCompraView(request,id):
    request.session['idorden'] = id 
    orden = OrdenCompra.objects.get(id=id)
    if (orden.despacho).strip() =='':
        return redirect('crea_detalle_orden_compra',id)
    else:
        mensaje1="Esta Orden tiene Despacho,"
        mensaje2 = 'No Se Puede Modificar'
        mensaje3 = ''
        return render(request,'compras/mensaje_editar_orden_compra.html',{'mensaje1':mensaje1,'mensaje2':mensaje2})


def CreaDetalleOrdenCompraView(request,id):
    request.session['idorden'] = id
    return redirect('selecciona_item_orden_compra',id)

def GuardaIdOrden(request):
    idorden = request.GET.get('id', None)
    orden_compra = OrdenCompra.objects.get(id=idorden)
    request.session['idproveedor'] = orden_compra.IdProveedor_id 
    request.session['idorden'] = idorden 
    data={'a':0}
    return JsonResponse(data)    

def GuardaIdOrdenCompraDetalle(request):
    idorden_detalle = request.GET.get('id', None)
    orden_detalle = OrdenCompraDetalle.objects.get(id=idorden_detalle)
    request.session['id_item_anterior'] = orden_detalle.IdItem_id 
    request.session['id_orden_detalle'] = idorden_detalle
    request.session['numero_orden'] = orden_detalle.numero
    data={'a':0}
    return JsonResponse(data) 

def DireccionaOrdenCompraView(request,id):
    if id == 1:
        idorden = request.session['idorden']
        return redirect('detalle_orden_compra',idorden)
    

def DespachosListView(request):
    queryset = Despacho.objects.all().order_by('-numero')
    f =  DespachoFilter(request.GET, queryset=queryset)
    despachos = DespachoTable(f.qs)
    request.session['filtro_iddepachos'] = False
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
    request.session['filtro_iddespachos'] = lista_id    
    despachos.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'despachos':despachos,'filter':f}
    return render(request, 'compras/despachos_lista.html', context) 

class CreaDespachoView(LoginRequiredMixin,CreateView):
    model = Despacho
    template_name = 'compras/despacho_form.html'
    form_class = DespachoForm

    def get_success_url(self):
        id = self.object.id
        return reverse_lazy('detalle_despacho', kwargs={'id': id})
    
    def get_initial(self,*args,**kwargs):
        initial=super(CreaDespachoView,self).get_initial(**kwargs)
        sucursal_defecto = ValorDefecto.objects.get(idValor='01')
        sucursal = Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
        initial['IdOrdenCompra'] = self.request.session['idorden']
        initial['IdProveedor'] = self.request.session['idproveedor']
        initial['IdSucursal'] = sucursal.id
        #bodega_defecto = ValorDefecto.objects.get(idValor='05')
        #bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
        #initial['IdBodega'] = bodega.id
        idproveedor = self.request.session['idproveedor']
        initial['IdProveedor'] = idproveedor
        initial['fecha'] = date.today()
        return initial
    
    def form_valid(self, form):
        if form.is_valid():
            tipodocumento = TipoDocumentoCompra.objects.get(idTipo='02')
            anumero = tipodocumento.actual +1
            snumero = str(anumero).zfill(tipodocumento.longitud)
            snumero = (tipodocumento.caracteres).strip()+snumero
            despacho = form.save(commit=False)
            despacho.IdUsuario_id = self.request.user.id
            despacho.numero = snumero
            despacho.IdTipoDocumento_id = tipodocumento.id
            despacho.estado = True
            despacho.save()
            despacho = Despacho.objects.get(numero=snumero)
            OrdenCompra.objects.filter(id=despacho.IdOrdenCompra_id).update(despacho=snumero)
            year = despacho.fecha
            anio = year.year
            mes = year.month
            tipo='06'
            #bodega_defecto = ValorDefecto.objects.get(idValor='05')
            #bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
            sucursal_defecto = ValorDefecto.objects.get(idValor='01')
            sucursal = Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
            orden = OrdenCompra.objects.get(id=despacho.IdOrdenCompra_id)
            idusuario = self.request.user.id
            InventariosViews.CreaDocumentoEntradaInventariosCabeza(despacho.fecha,tipo,anio,mes,orden.numero,orden.numero,snumero,orden.IdProveedor_id,despacho.detalle,idusuario)
            TipoDocumentoCompra.objects.filter(idTipo='02').update(actual = anumero)
            return redirect('despachos_list')   


class BuscaOrdenCompraDespacho(SingleTableMixin,FilterView):
    table_class = OrdenCompraListaTable
    model = OrdenCompra
    template_name = "compras/orden_compra_filter.html"
    filterset_class = OrdenCompraFilter1
    paginate_by = 8

def SeleccionaOrdenCompra(request):
    idOrden = request.GET.get('id', None)
    print('Id orden:',idOrden)
    orden = OrdenCompra.objects.get(id=idOrden)
    orden_compra = OrdenCompra.objects.get(id=idOrden)
    request.session['idorden'] = idOrden
    request.session['idproveedor'] = orden_compra.IdProveedor_id
    data = {'id':idOrden}
    return JsonResponse(data)
    

def ValidaCreaDespachoView(request):
    idOrden =request.session['idorden'] 
    orden = OrdenCompra.objects.get(id=idOrden)
    if (orden.despacho).strip() =='':
        orden_compra = OrdenCompra.objects.get(id=idOrden)
        return redirect('crea_despacho')
    else:
        mensaje1="Esta Orden ya tiene Despacho"
        mensaje2 = ''
        mensaje3 = ''
        return render(request,'compras/mensaje_despacho_ya_creado.html',{'mensaje1':mensaje1})
    
    
class EditaDespachoView(LoginRequiredMixin,UpdateView):
    model = Despacho
    fields = ['fecha','IdOrdenCompra','IdProveedor','detalle','IdSucursal']
    template_name = 'compras/despacho_form.html'
    success_url = reverse_lazy('despachos_list')

def ConfirmaBorradoDespachoView(request,id):
    request.session['iddespacho'] = id
    mensaje1="Esta seguro de borrar este despacho"
    mensaje2 = ''
    mensaje3 = ''
    return render(request,'compras/mensaje_confirma_borra_despacho.html',{'mensaje1':mensaje1})

def BorraDespachoView(request,id):
    if id == 1:
        iddespacho = request.session['iddespacho']
        despacho = Despacho.objects.get(id=iddespacho)
        despacho_detalle = DetalleDespacho.objects.filter(numero=despacho.numero)
        year = despacho.fecha
        anio = year.year
        mes = year.month
        invinic = False
        for desp in despacho_detalle:
            EntradaDetalle.objects.filter(despacho_detalle_id=desp.id).delete()
            Entrada.objects.filter(despacho=despacho.numero).delete()
            InventariosViews.ReversaAcumuladosEntradaInventarios(desp.IdItem_id,desp.cantidad_enviada,mes,anio,invinic)
            DetalleDespacho.objects.filter(id=desp.id).delete()
        Despacho.objects.filter(id=iddespacho).delete()
        OrdenCompra.objects.filter(despacho=despacho.numero).update(despacho='')
    return redirect('despachos_list')

def DetalleDespachoView(request,id):
    request.session['filtro_iddepachos'] = True
    request.session['iddespacho']=id
    lista_id = []
    lista_id.append(id)
    request.session['filtro_iddespachos'] = lista_id  
    despacho = DespachoTable(Despacho.objects.filter(id=id))
    detalle_despacho = DespachoDetalleTable(DetalleDespacho.objects.filter(IdDespacho_id=id))
    context = {'despacho':despacho,'detalle_despacho':detalle_despacho}
    return render(request, 'compras/detalle_despacho.html', context) 

def GuardaIdDespacho(request):
    iddespacho = request.GET.get('id', None)
    request.session['iddespacho'] = iddespacho
    despacho = Despacho.objects.get(id=iddespacho)
    request.session['idproveedor'] = despacho.IdProveedor_id 
    data={'a':0}
    return JsonResponse(data)    

def GuardaIdDespachoDetalle(request):
    iddespacho_detalle = request.GET.get('id', None)
    despacho_detalle = DetalleDespacho.objects.get(id=iddespacho_detalle)
    request.session['id_item_anterior'] = despacho_detalle.IdItem_id 
    request.session['id_despacho_detalle'] = iddespacho_detalle
    request.session['cantidad_anterior'] = despacho_detalle.cantidad
    request.session['numero_despacho'] = despacho_detalle.numero
    data={'a':0}
    return JsonResponse(data) 


def VerificaDetalleDespachoView(request,id):
    request.session['iddespacho'] = id
    if DetalleDespacho.objects.filter(IdDespacho_id=id).exists():
       return redirect('detalle_despacho',id)
    else:
        return redirect('crea_detalle_despacho',id)

def CreaDetalleDespachoView(request,id):
    despacho = Despacho.objects.get(id=id)
    orden = OrdenCompra.objects.get(id=despacho.IdOrdenCompra_id)
    detalle_orden = OrdenCompraDetalle.objects.filter(numero=orden.numero)
    detalle_despacho = DetalleDespacho()
    for orden in detalle_orden:
        idtipodoc = TipoDocumentoCompra.objects.get(idTipo='02')
        detalle_despacho.numero = despacho.numero
        detalle_despacho.IdDespacho_id = id
        detalle_despacho.IdTipoDocumento_id = idtipodoc.id
        detalle_despacho.IdItem_id = orden.IdItem_id
        detalle_despacho.estado = 1
        detalle_despacho.valor = orden.valor_compra
        detalle_despacho.cantidad_ordenada = orden.cantidad_empaque
        detalle_despacho.cantidad_enviada = orden.cantidad_empaque
        detalle_despacho.cantidad_unidades_enviadas=orden.cantidad_unidades_compra
        detalle_despacho.cantidad_unidad_empaque = orden.cantidad_unidad_empaque
        detalle_despacho.valor_unitario = orden.valor_unidad_empaque     
        #detalle_despacho.valor_total = int(float(orden.valor_compra))*int(float(orden.cantidad_empaque))
        detalle_despacho.valor_total = int(float(orden.valor_compra))
        detalle_despacho.save()
        detalle_despacho.id +=1 
        Detalle_despacho = DetalleDespacho.objects.latest('id')
        id_detalle_despacho = Detalle_despacho.id
        tipo = '06'
        year = despacho.fecha
        anio = year.year
        mes = year.month
        #bodega_defecto = ValorDefecto.objects.get(idValor='05')
        #bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
        #sucursal_defecto = ValorDefecto.objects.get(idValor='01')
        #sucursal = Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
        #orden = OrdenCompra.objects.get(id=despacho.IdOrdenCompra_id)
        idusuario = request.user.id
        entrada = Entrada.objects.get(despacho=despacho.numero)
        valor_total = int(float(orden.valor_compra))*int(float(orden.cantidad_empaque))
        items_despacho = DetalleDespacho.objects.filter(numero=despacho.numero)
        #val_tot = 0
        #for item in items_despacho:
        #    val_tot = val_tot + item.cantidad_enviada*item.valor
        OrdenCompra.objects.filter(id=despacho.IdOrdenCompra_id).update(despacho=despacho.numero)
        InventariosViews.CreaDocumentoEntradaCuerpo(tipo,anio,mes,entrada.numero,orden.IdItem_id,orden.cantidad_unidades_compra,orden.valor_unitario,orden.valor_compra,id_detalle_despacho)
    return redirect('detalle_despacho',id)    


def DatosDespachoDetalleView(request):
    iddespacho_detalle = request.GET.get('iddetalle', None)
    despacho_detalle = DetalleDespacho.objects.get(id=iddespacho_detalle)
    request.session['id_item_anterior'] = despacho_detalle.IdItem_id 
    request.session['id_despacho_detalle'] = iddespacho_detalle
    request.session['cantidad_enviada_anterior'] = despacho_detalle.cantidad_enviada
    request.session['numero_despacho'] = despacho_detalle.numero
    data={'registro':iddespacho_detalle}
    return JsonResponse(data) 
    
def DatosEmpaqueView(request):
    id = request.GET.get('id', None)
    id = int(id)
    empaques = EmpaqueItemTable(EmpaqueItem.objects.filter(IdItem_id=id))
    context = {'empaques': empaques}
    html_form = render_to_string('compras/empaques_lista.html',
        context,
        request=request,
    )
    print('Html Form:',html_form)
    return JsonResponse({'html_form': html_form})

def GuardaCantidadEnviadaView(request):
    cantidad_enviada = request.GET.get('cantidad_enviada', None)
    cantidad_enviada = int(cantidad_enviada)
    id_despacho_detalle = request.session['id_despacho_detalle']
    request.session['iddespacho'] = id_despacho_detalle
    id_item_anterior = request.session['id_item_anterior']
    cantidad_enviada_anterior = request.session['cantidad_enviada_anterior']
    detalle_despacho = DetalleDespacho.objects.get(id=id_despacho_detalle)
    despacho = Despacho.objects.get(id=detalle_despacho.IdDespacho_id)   
    orden = OrdenCompra.objects.get(id=despacho.IdOrdenCompra_id)
    orden_detalle = OrdenCompraDetalle.objects.get(IdItem_id=id_item_anterior)
    year = despacho.fecha
    anio = year.year
    mes = year.month
    invinic = False
    cantidad_unidad_empaque = orden_detalle.cantidad_unidad_empaque
    cantidad_en_unidades_anterior = cantidad_enviada_anterior* cantidad_unidad_empaque
    cantidad_en_unidades_nueva = cantidad_enviada* cantidad_unidad_empaque
    #print('Antes:',cantidad_en_unidades_anterior)
    #print('Ahora:',cantidad_en_unidades_nueva)
    InventariosViews.ReversaAcumuladosEntradaInventarios(id_item_anterior,cantidad_en_unidades_anterior,mes,anio,invinic)
    InventariosViews.ActualizaAcumuladosInventarios(id_item_anterior,cantidad_en_unidades_nueva,(detalle_despacho.valor_total/cantidad_en_unidades_anterior),mes,anio,'entrada',1,invinic)
    detalle_despacho = DetalleDespacho.objects.get(id=id_despacho_detalle)
    valor_total = cantidad_enviada* detalle_despacho.valor_unitario
    DetalleDespacho.objects.filter(id=id_despacho_detalle).update(cantidad_enviada=cantidad_enviada,cantidad_unidades_enviadas=cantidad_enviada*orden_detalle.cantidad_unidad_empaque,cantidad_unidad_empaque=orden_detalle.cantidad_unidad_empaque,valor_total=valor_total)
    EntradaDetalle.objects.filter(despacho_detalle_id=id_despacho_detalle).update(cantidad=cantidad_enviada*cantidad_unidad_empaque,valor_total=valor_total)
    MaestroItem.objects.filter(id= id_item_anterior).update(valor_compra=orden_detalle.valor_unitario)
    data={'cantidad_enviada':cantidad_enviada,'registro':despacho.id,'valor_total':valor_total}
    return JsonResponse(data) 

    
def DireccionaDespachoView(request,id):
    if id == 1:
        iddespacho = request.session['iddespacho']
        return redirect('detalle_despacho',iddespacho)    

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from  reportlab.lib.styles import ParagraphStyle

style = getSampleStyleSheet()['Normal']

def P(txt):
    return Paragraph(txt, style)


def ProveedorItemView(request):
    proveedor_item = ProveedorItem()
    ProveedorItem.objects.all().delete()
    ordenes = OrdenCompra.objects.all().order_by('-fecha')
    for orden in ordenes:
        idproveedor = orden.IdProveedor_id
        detalle_orden = OrdenCompraDetalle.objects.filter(numero=orden.numero)
        for detalle in detalle_orden:
            if not ProveedorItem.objects.filter(IdProveedor_id=idproveedor,IdItem_id=detalle.IdItem_id).exists():    
                item =  detalle.IdItem_id
                proveedor_item.IdItem_id = item
                proveedor_item.IdProveedor_id = idproveedor 
                proveedor_item.save()
                proveedor_item.id +=1 
    
    queryset = ProveedorItem.objects.all()
    f =  ProveedorItemFilter(request.GET, queryset=queryset)
    proveedor_item = ProveedorItemTable(f.qs)
    request.session['filtro_item_proveedor_id'] = False
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
    request.session['filtro_item_proveedor_id'] = lista_id    
    proveedor_item.paginate(page=request.GET.get("page", 1), per_page=20)
    context = {'proveedor_item':proveedor_item,'filter':f}
    return render(request, 'compras/proveedor_item_lista.html', context) 

def ImpresionOrdenesCompraView(request):
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
    pdf.drawString(200, y, u"ORDENES DE COMPRA")
    pdf.setFont("Helvetica", 9)
    y -= 50
    sw = 0
    if request.session['filtro_idordenes']:
        idordenes = request.session['filtro_idordenes']
        #ordenes = OrdenCompra.objects.filter(id__in=idordenes)
        ordenes = OrdenCompra.objects.filter(id__in=idordenes).annotate(proveedor_nombre=Concat(F('IdProveedor__apenom'),Value(' '),F('IdProveedor__razon_social'),output_field=CharField()))
    else:
        #ordenes = OrdenCompra.objects.all()
        ordenes = OrdenCompra.objects.all().annotate(proveedor_nombre=Concat(F('IdProveedor__apenom'),Value(' '),F('IdProveedor__razon_social'),output_field=CharField()) )
    for orden in ordenes:
        encabezados =('Fecha','Número','Proveedor','Despacho','Detalle','Estado','Valor','Usuario')
        detalle = [(orden.fecha,orden.numero,(orden.proveedor_nombre[0:38]),orden.despacho,orden.detalle,orden.estado,'{:,}'.format(orden.valor),orden.IdUsuario)]
        detalle_orden = Table([encabezados] + detalle, colWidths=[1.5 * cm,1.5 * cm,6 * cm,1.5 * cm,4.2 * cm,1.2 * cm,2 * cm,1.5 * cm])
        detalle_orden.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1),7),
        ]
        ))
        pdf.setFont("Helvetica", 7)    
        detalle_orden.wrapOn(pdf, 300, 800)
        detalle_orden.drawOn(pdf, 20,y)
        y -= 35
        orden_detalle = OrdenCompraDetalle.objects.filter(numero=orden.numero)
        encabezados =('Item','Cant.Emp.','Val.Unid.Emp.','Cant.Unid.emp.','Cant.Unid.Compra','Unid.Med','Valor Compra')
        orden_detalle = OrdenCompraDetalle.objects.filter(numero=orden.numero)
        detalle = [(ordendet.IdItem.descripcion[0:43],'{:,}'.format(ordendet.cantidad_empaque),'{:,}'.format(ordendet.valor_unidad_empaque),'{:,}'.format(ordendet.cantidad_unidad_empaque),'{:,}'.format(ordendet.cantidad_unidades_compra),ordendet.IdItem.IdUnidadMedida,'{:,}'.format(ordendet.valor_compra)) for ordendet in orden_detalle]
        detalle_ordendet = Table([encabezados] + detalle, colWidths=[6 * cm,1.5 * cm,1.8 * cm,2.0 * cm,2.3 * cm,2.8 * cm,3.0 * cm,2.0 * cm])
        detalle_ordendet.setStyle(TableStyle(
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
        y = y - b*16
        if y<= 30:
            pdf.showPage()
            y= 750
        pdf.setFont("Helvetica", 7)    
        detalle_ordendet.wrapOn(pdf, 300, 800)
        detalle_ordendet.drawOn(pdf, 20,y)
        y -= 40
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionDetalleOrdenCompraPdfView(request):
    id=request.session['idorden']
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
    pdf.drawString(200, y, u"ORDEN DE COMPRA")
    pdf.setFont("Helvetica", 9)
    y -= 50
    sw = 0
    ordenes = OrdenCompra.objects.filter(id=id)
    ordenes = Despacho.objects.filter(id=id).annotate(proveedor_nombre=Concat(F('IdProveedor__apenom'),Value(' '),F('IdProveedor__razon_social'),output_field=CharField()) )
    for orden in ordenes:
        encabezados =('Fecha','Número','Proveedor','Despacho','Detalle','Estado','Valor','Usuario')
        detalle = [(orden.fecha,orden.numero,(orden.IdProveedor.razon_social),orden.despacho,orden.detalle,orden.estado,'{:,}'.format(orden.valor),orden.IdUsuario)]
        detalle_orden = Table([encabezados] + detalle, colWidths=[1.5 * cm,1.5 * cm,5 * cm,1.5 * cm,5.2 * cm,1.2 * cm,2 * cm,1.5 * cm])
        detalle_orden.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1),7),
        ]
        ))
        pdf.setFont("Helvetica", 7)    
        detalle_orden.wrapOn(pdf, 300, 800)
        detalle_orden.drawOn(pdf, 20,y)
        y -= 22
        encabezados =('Item','Cant.Emp.','Val.Unid.Emp.','Cant.Unid.emp.','Cant.Unid.Compra','Unid.Med','Valor Compra')
        orden_detalle = OrdenCompraDetalle.objects.filter(numero=orden.numero)
        detalle = [(ordendet.IdItem.descripcion[0:43],'{:,}'.format(ordendet.cantidad_empaque),'{:,}'.format(ordendet.valor_unidad_empaque),'{:,}'.format(ordendet.cantidad_unidad_empaque),'{:,}'.format(ordendet.cantidad_unidades_compra),ordendet.IdItem.IdUnidadMedida,'{:,}'.format(ordendet.valor_compra)) for ordendet in orden_detalle]
        detalle_ordendet = Table([encabezados] + detalle, colWidths=[6 * cm,1.5 * cm,1.8 * cm,2.0 * cm,2.3 * cm,2.8 * cm,3.0 * cm,2.0 * cm])
        detalle_ordendet.setStyle(TableStyle(
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
            y= 750
        pdf.setFont("Helvetica", 7)    
        detalle_ordendet.wrapOn(pdf, 300, 800)
        detalle_ordendet.drawOn(pdf, 20,y)
        y -= 50
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionOrdenesCompraXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    if request.session['filtro_idordenes']:
        idordenes = request.session['filtro_idordenes']
        ordenes = OrdenCompra.objects.filter(id__in=idordenes)
    else:    
        ordenes = OrdenCompra.objects.all()
    n=1
    for orden in ordenes:
        nn = str(n)
        exec("worksheet.write('A"+nn+"','Fecha')" )
        exec("worksheet.write('B"+nn+"','Número')" )
        exec("worksheet.write('C"+nn+"','Proveedor')")
        exec("worksheet.write('D"+nn+"','Despacho')")
        exec("worksheet.write('E"+nn+"','Detalle')")
        exec("worksheet.write('F"+nn+"','Estado')")
        exec("worksheet.write('G"+nn+"','Valor')")
        n = n+1
        nn = str(n)
        exec("worksheet.write('A"+nn+"','"+orden.fecha.strftime("%d/%m/%Y")+"' )")
        exec("worksheet.write('B"+nn+"','"+orden.numero+"' )")
        proveedor = Proveedor.objects.get(id=orden.IdProveedor_id)
        exec("worksheet.write('C"+nn+"','"+proveedor.apenom+"' )")
        exec("worksheet.write('D"+nn+"','"+orden.despacho+"' )")
        exec("worksheet.write('E"+nn+"','"+orden.detalle+"' )")
        exec("worksheet.write('F"+nn+"','"+str(orden.estado)+"' )")
        exec("worksheet.write('G"+nn+"','"+str(orden.valor)+"' )")
        #exec("worksheet.write('H"+nn+"','"+orden.IdBodega.descripcion+"' )")
        orden_detalle = OrdenCompraDetalle.objects.filter(numero=orden.numero)
        n = n+1
        nn = str(n)
        
        exec("worksheet.write('A"+nn+"','Número')" )
        exec("worksheet.write('B"+nn+"','Item')")
        exec("worksheet.write('C"+nn+"','Cant.Empaque')")
        exec("worksheet.write('D"+nn+"','Valor Unit.Emp.')")
        exec("worksheet.write('E"+nn+"','Cant.Unid.Emp')")
        exec("worksheet.write('F"+nn+"','Cant.Unid.Compra')")
        exec("worksheet.write('G"+nn+"','Unid.Med')")
        exec("worksheet.write('H"+nn+"','Valor Compra')")
        for detalle in orden_detalle:
            n= n+1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','"+detalle.numero+"' )")
            exec("worksheet.write('B"+nn+"','"+detalle.IdItem.descripcion+"' )")
            exec("worksheet.write('C"+nn+"','"+str(detalle.cantidad_empaque)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(detalle.valor_unidad_empaque)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(detalle.cantidad_unidad_empaque)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(detalle.cantidad_unidades_compra)+"' )")
            idunidad = detalle.IdItem.IdUnidadMedida_id
            unidad_medida = Medida.objects.get(id=idunidad) 
            exec("worksheet.write('G"+nn+"','"+unidad_medida.descripcion+"' )")
            exec("worksheet.write('H"+nn+"','"+str(detalle.valor_compra)+"' )")          
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'ordenes_compra.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response

def ImpresionDetalleOrdenCompraXlsView(request):
    id=request.session['idorden']
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    ordenes = OrdenCompra.objects.filter(id=id)
    n=1
    for orden in ordenes:
        nn = str(n)
        exec("worksheet.write('A"+nn+"','Fecha')" )
        exec("worksheet.write('B"+nn+"','Número')" )
        exec("worksheet.write('C"+nn+"','Proveedor')")
        exec("worksheet.write('D"+nn+"','Despacho')")
        exec("worksheet.write('E"+nn+"','Detalle')")
        exec("worksheet.write('F"+nn+"','Estado')")
        exec("worksheet.write('G"+nn+"','Valor')")
        exec("worksheet.write('H"+nn+"','Bodega')")
        n = n+1
        nn = str(n)
        exec("worksheet.write('A"+nn+"','"+orden.fecha.strftime("%d/%m/%Y")+"' )")
        exec("worksheet.write('B"+nn+"','"+orden.numero+"' )")
        exec("worksheet.write('C"+nn+"','"+orden.IdProveedor.razon_social+"' )")
        exec("worksheet.write('D"+nn+"','"+orden.despacho+"' )")
        exec("worksheet.write('E"+nn+"','"+orden.detalle+"' )")
        exec("worksheet.write('F"+nn+"','"+str(orden.estado)+"' )")
        exec("worksheet.write('G"+nn+"','"+str(orden.valor)+"' )")
        #exec("worksheet.write('H"+nn+"','"+orden.IdBodega.descripcion+"' )")
        orden_detalle = OrdenCompraDetalle.objects.filter(numero=orden.numero)
        n = n+1
        nn = str(n)
        
        exec("worksheet.write('A"+nn+"','Número')" )
        exec("worksheet.write('D"+nn+"','Item')")
        exec("worksheet.write('E"+nn+"','Valor')")
        exec("worksheet.write('F"+nn+"','Cantidad')")
        exec("worksheet.write('G"+nn+"','Valor Total')")
        for detalle in orden_detalle:
            n= n+1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','"+detalle.numero+"' )")
            exec("worksheet.write('C"+nn+"','"+str(detalle.estado)+"' )")
            exec("worksheet.write('D"+nn+"','"+detalle.IdItem.descripcion+"' )")
            exec("worksheet.write('E"+nn+"','"+str(detalle.valor)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(detalle.cantidad)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(detalle.valor_total)+"' )")          
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'ordenes_compra.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response

def ImpresionDespachoView(request):
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
    pdf.drawString(220, y, u"DESPACHOS")
    pdf.setFont("Helvetica", 9)
    y -= 50
    sw = 0
    if request.session['filtro_iddespachos']:
        iddespachos = request.session['filtro_iddespachos']
        #despachos = Despacho.objects.filter(id__in=iddespachos)
        despachos = Despacho.objects.filter(id__in=iddespachos).annotate(proveedor_nombre=Concat(F('IdProveedor__apenom'),Value(' '),F('IdProveedor__razon_social'),output_field=CharField()) )
    else:
        #despachos = Despacho.objects.all()
        despachos = Despacho.objects.all().annotate(proveedor_nombre=Concat(F('IdProveedor__apenom'),Value(' '),F('IdProveedor__razon_social'),output_field=CharField()) )
    for despacho in despachos:
        encabezados =('Fecha','Número','Proveedor','Orden Compra','Detalle','Estado','Usuario')
        detalle = [(despacho.fecha,despacho.numero,despacho.proveedor_nombre[0:30],despacho.IdOrdenCompra,despacho.detalle[0:30],despacho.estado,despacho.IdUsuario)]
        detalle_despacho = Table([encabezados] + detalle, colWidths=[1.5 * cm,1.5 * cm,5.3 * cm,3 * cm,5.5 * cm,1.2 * cm,2 * cm,1.5 * cm])
        detalle_despacho.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1),7),
        ]
        ))
        pdf.setFont("Helvetica", 7)    
        detalle_despacho.wrapOn(pdf, 300, 800)
        detalle_despacho.drawOn(pdf, 20,y)
        y -= 10
        despacho_detalle = DetalleDespacho.objects.filter(numero=despacho.numero)
         
        encabezados =('Item','Cantidad Ord.','Cantidad Env.','Cant.Unid.Emp.','Cant.Unid.Env.','Valor Unit.','Valor Total')
        detalle = [((despdet.IdItem.descripcion[0:38]),'{:,}'.format(despdet.cantidad_ordenada),'{:,}'.format(despdet.cantidad_enviada),'{:,}'.format(despdet.cantidad_unidad_empaque),'{:,}'.format(despdet.cantidad_unidades_enviadas),'{:,}'.format(despdet.valor_unitario),'{:,}'.format(despdet.valor_total)) for despdet in despacho_detalle]
        detalle_ordendet = Table([encabezados] + detalle, colWidths=[5 * cm,2.5 * cm,2.5 * cm,2.5 * cm,2.5 * cm,2.5 * cm])
        detalle_ordendet.setStyle(TableStyle(
        [
            #La primera fila(encabezados) va a estar centrada
            ('ALIGN',(0,0),(3,0),'CENTER'),
            #Los bordes de todas las celdas serán de color negro y con un grosor de 1
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            #El tamaño de las letras de cada una de las celdas será de 10
            ('FONTSIZE', (0, 0), (-1, -1),7),
        ]
        ))
        b= 1
        for j in detalle:
            y = y - b*25
        if y<= 35:
            pdf.showPage()
            y= 750
        pdf.setFont("Helvetica", 7)    
        detalle_ordendet.wrapOn(pdf, 300, 800)
        detalle_ordendet.drawOn(pdf, 20,y)
        y -= 60
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionDespachoXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    if request.session['filtro_iddespachos']:
        iddespachos = request.session['filtro_iddespachos']
        despachos = Despacho.objects.filter(id__in=iddespachos)
    else:    
        despachos = Despacho.objects.all()
    n=1
    for despacho in despachos:
        nn = str(n)
        exec("worksheet.write('A"+nn+"','Fecha')" )
        exec("worksheet.write('B"+nn+"','Número')" )
        exec("worksheet.write('C"+nn+"','Proveedor')")
        exec("worksheet.write('D"+nn+"','Orden Compra')")
        exec("worksheet.write('E"+nn+"','Detalle')")
        exec("worksheet.write('F"+nn+"','Estado')")
        exec("worksheet.write('G"+nn+"','Bodega')")
        exec("worksheet.write('H"+nn+"','Usuario')")
        n = n+1
        nn = str(n)
        exec("worksheet.write('A"+nn+"','"+despacho.fecha.strftime("%d/%m/%Y")+"' )")
        exec("worksheet.write('B"+nn+"','"+despacho.numero+"' )")
        exec("worksheet.write('C"+nn+"','"+despacho.IdProveedor.razon_social+"' )")
        exec("worksheet.write('D"+nn+"','"+despacho.IdOrdenCompra.numero+"' )")
        exec("worksheet.write('E"+nn+"','"+despacho.detalle+"' )")
        exec("worksheet.write('F"+nn+"','"+str(despacho.estado)+"' )")
        #exec("worksheet.write('G"+nn+"','"+despacho.IdBodega.descripcion+"' )")
        exec("worksheet.write('H"+nn+"','"+despacho.IdUsuario.username+"' )")
        despacho_detalle = DetalleDespacho.objects.filter(numero=despacho.numero)
        n = n+1
        nn = str(n)
        
        exec("worksheet.write('A"+nn+"','Número')" )
        exec("worksheet.write('B"+nn+"','Item')")
        exec("worksheet.write('C"+nn+"','Cantidad Ordenada')")
        exec("worksheet.write('D"+nn+"','Cantidad Enviada')")
        exec("worksheet.write('E"+nn+"','Cantidad Unid. Por Empaque')")
        exec("worksheet.write('F"+nn+"','Cantidad Unid. Enviadas')")
        exec("worksheet.write('G"+nn+"','Valor Total')")
        for detalle in despacho_detalle:
            n= n+1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','"+detalle.numero+"' )")
            exec("worksheet.write('B"+nn+"','"+detalle.IdItem.descripcion+"' )")
            exec("worksheet.write('C"+nn+"','"+str(detalle.cantidad_ordenada)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(detalle.cantidad_enviada)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(detalle.cantidad_unidad_empaque)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(detalle.cantidad_unidades_enviadas)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(detalle.valor_total)+"' )")          
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'despachos.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response

def ImpresionProveedoresXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1','Identificacion' )
    worksheet.write('B1','Tipo Identificacion' )
    worksheet.write('C1','Nombre 1' )
    worksheet.write('D1','Nombre 2' )
    worksheet.write('E1','Apellido 1' )
    worksheet.write('F1','Apellido 2' )
    worksheet.write('G1','Razon Social' )
    worksheet.write('H1','Apenom' )
    worksheet.write('I1','Direccion' )
    worksheet.write('J1','Telefono' )
    worksheet.write('K1','Email' )
    worksheet.write('L1','Contacto' )
    worksheet.write('M1','Pais' )
    worksheet.write('N1','Departamento' )
    worksheet.write('O1','Ciudad' )
    worksheet.write('P1','Por Ica' )
    worksheet.write('Q1','Por Ret Fte' )
    n = 2
    if request.session['filtro_proveedores_id']:
        id_proveedores = request.session['filtro_proveedores_id']       
        proveedores =Proveedor.objects.filter(id__in=id_proveedores)
    else:
        proveedores = Proveedor.objects.all()    
    for j in proveedores: 
        nn = str(n)
        pais = j.IdPais.descripcion
        if j.razon_social == None:
            razon_social = ''
        else:
            razon_social = j.razon_social    
        exec("worksheet.write('A"+nn+"','"+j.identificacion+"' )")
        exec("worksheet.write('B"+nn+"','"+j.IdTipoIdentificacion.descripcion+"' )")
        exec("worksheet.write('C"+nn+"','"+j.nombre1+"' )")
        exec("worksheet.write('D"+nn+"','"+j.nombre2+"' )")
        exec("worksheet.write('E"+nn+"','"+j.apel1+"' )")
        exec("worksheet.write('F"+nn+"','"+j.apel2+"' )")
        exec("worksheet.write('G"+nn+"','"+razon_social+"' )")
        exec("worksheet.write('H"+nn+"','"+j.apenom+"' )")
        exec("worksheet.write('I"+nn+"','"+j.direccion+"' )")
        exec("worksheet.write('J"+nn+"','"+j.telefono+"' )")
        exec("worksheet.write('K"+nn+"','"+str(j.email)+"' )")
        exec("worksheet.write('L"+nn+"','"+j.contacto+"' )")
        exec("worksheet.write('M"+nn+"','"+pais+"' )")
        exec("worksheet.write('N"+nn+"','"+j.departamento+"' )")
        exec("worksheet.write('O"+nn+"','"+j.ciudad+"' )")
        exec("worksheet.write('P"+nn+"','"+str(j.por_ica)+"' )")
        exec("worksheet.write('Q"+nn+"','"+str(j.por_ret_fte)+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'proveedores.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response

def ImpresionItemProveedorView(request):
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
    pdf.drawString(200, y, u"ITEM PROVEEDOR")
    pdf.setFont("Helvetica", 9)
    y -= 50
    sw = 0
    if request.session['filtro_item_proveedor_id']:
        id_item_proveedor = request.session['filtro_item_proveedor_id']
        item_proveedores = ProveedorItem.objects.filter(id__in=id_item_proveedor)
        registros = ProveedorItem.objects.filter(id__in=id_item_proveedor).count()
    else:
        item_proveedores = ProveedorItem.objects.all()
        registros = ProveedorItem.objects.all().count()
    print(item_proveedores)
    encabezados =('Proveedor','Item')
    cuerpo = [(f"{item.IdProveedor.apenom} {item.IdProveedor.razon_social}",item.IdItem.descripcion) for item in item_proveedores ]
    cuerpo_rep = Table([encabezados] + cuerpo, colWidths=[8 * cm,8 * cm])
    cuerpo_rep.setStyle(TableStyle(
    [
        #La primera fila(encabezados) va a estar centrada
        ('ALIGN',(0,0),(3,0),'CENTER'),
        #Los bordes de todas las celdas serán de color negro y con un grosor de 1
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        #El tamaño de las letras de cada una de las celdas será de 10
        ('FONTSIZE', (0, 0), (-1, -1),7),
    ]
    ))
    pdf.setFont("Helvetica", 7)    
    y = y - registros*18
    if y<= 30:
        pdf.showPage()
        y= 750
    cuerpo_rep.wrapOn(pdf, 300, 800)
    cuerpo_rep.drawOn(pdf, 20,y)
    pdf.setFont("Helvetica", 7)    
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionItemProveedorXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1','Proveedor' )
    worksheet.write('B1','Articulo' )
    n = 2
    if request.session['filtro_item_proveedor_id']:
        id_item_proveedor = request.session['filtro_item_proveedor_id']       
        item_proveedores = ProveedorItem.objects.filter(id__in=id_item_proveedor)
    else:
        item_proveedores = ProveedorItem.objects.all()
    for j in item_proveedores: 
        nn = str(n)
        nombre_proveedor =f"{j.IdProveedor.apenom} {j.IdProveedor.razon_social}"
        exec("worksheet.write('A"+nn+"','"+nombre_proveedor+"' )")
        exec("worksheet.write('B"+nn+"','"+j.IdItem.descripcion+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'Item_Proveedor.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response