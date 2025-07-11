from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from datetime import timedelta,date
from django_tables2.views import SingleTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.db.models import F, ExpressionWrapper, DecimalField,IntegerField,Subquery, OuterRef

from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest,HttpResponse, HttpRequest, JsonResponse,HttpResponseRedirect
from django.core import serializers
from django.core.serializers import serialize
from django.db.models import Q,Sum

from core.models import ValorDefecto,Sucursal,Empresa,Tercero,Anio,Mes
from compras.models import Proveedor,OrdenCompra,Despacho
from cocina.models import Ingrediente
from .models import Grupo,SubGrupo,Bodega,MaestroItem,AcumuladoItem,Medida,Salida,TipoDocumentoInv,SalidaDetalle,Entrada,EntradaDetalle,Kardex,InventarioFisico,AjusteInventarioFisico
from .models import CierreInventario
from .tables import GruposInventarioTable,SubGruposInventarioTable,BodegasInventarioTable,ItemsInventarioTable,ItemsInventarioTable1,ItemsInventarioTable2,MedidasInventarioTable,ItemsInventarioFisicoTable
from .tables import AcumuladoItemsInventarioTable,AcumuladoItemsInventarioTable1,AcumuladoItemsInventarioTable2,ItemsListaTable1,ItemsListaTable,EntradasInventarioDetalleTable,InventarioFisicoTable
from .tables import AcumuladoItemsInventarioTable3,AcumuladoItemsInventarioTable4,SalidasInventarioTable,SalidasInventarioDetalleTable,EntradasInventarioTable,KardexTable,KardexItemTable
from .forms import GruposInventariosForm,SubGruposInventariosForm,BodegasInventariosForm,ItemsInventariosForm,MedidasInventariosForm,AcumuladoItemsInventariosForm,EntradasInventariosForm
from .forms import SalidasInventariosForm,SalidasInventariosDetalleForm,EntradasInventariosForm,InventarioFisicoForm,AjusteInventariosForm,MesForm,AnioForm,Sucursal,BodegaForm,SucursalForm
from .filters import MaestroItemsFilter1,AcumuladoItemsInventarioFilter,SalidasInventarioFilter,MaestroItemsFilter,EntradasInventarioFilter,InventarioFisicoFilter,SubGrupoFilter
from caja.views import PedidoCaja,PedidoCajaDetalle
#from cocina.models import Ingrediente
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

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from  reportlab.lib.styles import ParagraphStyle
style = getSampleStyleSheet()['Normal']

def P(txt):
    return Paragraph(txt, style,bulletText=None)

class MenuProcesosInventario(TemplateView):
    template_name = "inventarios/menu_procesos_inventario.html"

def CreaDocumentoSalidaInventariosCabeza(fecha,tipo,anio,mes,numero,num_ped,detalle,idusuario):
    tipodocumentoinv = TipoDocumentoInv.objects.get(idTipo=tipo)
    anumero = tipodocumentoinv.actual +1
    salida = Salida()
    salida.numero = numero
    salida.IdTipoDocumento_id = tipodocumentoinv.id
    salida.fecha = fecha 
    salida.detalle = detalle
    salida.estado = True
    salida.valor = 0
    #salida.IdBodega_id = idbodega
    #salida.IdSucursal_id = idsucursal
    salida.IdUsuario_id = idusuario
    salida.pedido_caja = num_ped
    salida.anio = anio
    salida.save()
    TipoDocumentoInv.objects.filter(idTipo=tipo).update(actual=anumero)
    
        
def CreaDocumentoSalidaInventariosCuerpo(tipo,anio,mes,numero,num_ped,iditem,cantidad,valor_venta,valor_total):
    tipodocumentoinv = TipoDocumentoInv.objects.get(idTipo=tipo)
    salida = Salida.objects.get(numero=numero)
    salida_detalle = SalidaDetalle()
    salida_detalle.numero = numero
    salida_detalle.IdTipoDocumento_id = tipodocumentoinv.idTipo
    salida_detalle.IdSalida_id = salida.id
    salida_detalle.estado = True
    salida_detalle.IdItem_id = iditem
    item = MaestroItem.objects.get(id=iditem)
    salida_detalle.IdBodega_id = item.IdBodega_id
    salida_detalle.valor = valor_venta
    salida_detalle.cantidad = cantidad
    salida_detalle.valor_total = valor_total
    salida_detalle.save()
    invinic = False
    ActualizaAcumuladosInventarios(iditem,cantidad,0,mes,anio,'salida',0,invinic)
    

def CreaDocumentoEntradaInventariosCabeza(fecha,tipo,anio,mes,pnumero,orden_compra,despacho,IdTercero,detalle,idusuario):
    tipodocumentoinv = TipoDocumentoInv.objects.get(idTipo=tipo)
    anumero = tipodocumentoinv.actual +1
    entrada = Entrada()
    entrada.numero = pnumero
    entrada.IdTercero_id = IdTercero
    entrada.IdTipoDocumento_id = tipodocumentoinv.id
    entrada.fecha = fecha
    entrada.anio = anio 
    entrada.detalle = detalle
    entrada.estado = True
    entrada.valor = 0
    #entrada.IdBodega_id = idbodega
    #entrada.IdSucursal_id = idsucursal
    entrada.IdUsuario_id = idusuario
    entrada.orden_compra = orden_compra
    entrada.despacho = despacho
    entrada.save()
    TipoDocumentoInv.objects.filter(idTipo=tipo).update(actual=anumero)
    
        
def CreaDocumentoEntradaCuerpo(tipo,anio,mes,numero,iditem,cantidad,valor,valor_total,id_despacho_detalle):
    tipodocumentoinv = TipoDocumentoInv.objects.get(idTipo=tipo)
    entrada_detalle = EntradaDetalle()
    entrada = Entrada.objects.get(numero=numero)
    entrada_detalle.numero = entrada.numero
    entrada_detalle.IdTipoDocumento_id = tipodocumentoinv.idTipo
    entrada_detalle.IdEntrada_id = entrada.id
    entrada_detalle.estado = True
    entrada_detalle.IdItem_id = iditem
    item = MaestroItem.objects.get(id=entrada_detalle.IdItem_id)
    entrada_detalle.IdBodega_id = item.IdBodega_id
    entrada_detalle.valor = valor
    entrada_detalle.cantidad = cantidad
    entrada_detalle.valor_total = valor_total
    entrada_detalle.despacho_detalle_id = id_despacho_detalle
    entrada_detalle.save()
    if tipo == '03' or tipo == '06':
        costo = 1
    else:
        costo = 0  
    if tipo == '05':
        invinic = True
    else:
        invinic = False        
    ActualizaAcumuladosInventarios(iditem,cantidad,valor,mes,anio,'entrada',costo,invinic)

def ActualizaAcumuladosInventarios(iditem,cantidad,valor,mes,anio,topera,costo,invinic):
    item = MaestroItem.objects.get(id=iditem)
    idbodega = item.IdBodega_id
    if item.acumula == True:
        entradas = 0
        salidas = 0
        ###bodega_defecto = ValorDefecto.objects.get(idValor='05')
        ##bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
        sanio = str(anio)
        smes = mes
        cantidad = int(cantidad)
        acumula = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).exists()
        if acumula == False:
            bodegas = Bodega.objects.all()
            acumulado_item = AcumuladoItem()
            acumulado_item.IdItem_id = iditem
            #acumulado_item.IdSucursal_id = sucursal.id 
            acumulado_item.IdBodega_id = item.IdBodega_id
            acumulado_item.anio = sanio
            acumulado_item.save() 
        acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
        if smes == 1:
            inv_inic = acumulado.ii_01
            entradas = acumulado.ent_01
            salidas = acumulado.sal_01
            #inv_fin = acumulado.if_01
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_01=salidas,if_01=inv_final)
            else:
                if costo == 1:
                    costo_prom= valor
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)     
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:      
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_01=entradas,if_01=inv_final)
        if smes == 2:
            inv_inic = acumulado.if_01
            entradas = acumulado.ent_02
            salidas = acumulado.sal_02
            #inv_fialn = acumulado.if_02
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_02=salidas,ii_02=inv_inic,if_02=inv_final)
            else:
                if costo == 1:
                    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
                    d = acumulado.if_02*valor+cantidad*valor
                    s = acumulado.if_02 + acumulado.ent_02+cantidad
                    if s>0:
                        costo_prom = d/s
                    else:
                        costo_prom = 0    
                    costo_prom=int(costo_prom)
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)     
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:        
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_02=entradas,ii_02=inv_inic,if_02=inv_final)
            
        if smes == 3:
            inv_inic = acumulado.if_02
            entradas = acumulado.ent_03
            salidas = acumulado.sal_03
            #inv_final = acumulado.if_03
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_03=salidas,ii_03=inv_inic,if_03=inv_final)
            else:
                if costo == 1:
                    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
                    d = acumulado.if_03*valor+cantidad*valor
                    s = acumulado.if_03 + acumulado.ent_03+cantidad
                    if s>0:
                        costo_prom = d/s
                    else:
                        costo_prom = 0    
                    costo_prom=int(costo_prom)
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)     
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:        
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_03=entradas,ii_03=inv_inic,if_03=inv_final)
        if smes == 4:
            inv_inic = acumulado.if_03
            entradas = acumulado.ent_04
            salidas = acumulado.sal_04
            #inv_final = acumulado.if_04
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_04=salidas,ii_04=inv_inic,if_04=inv_final)
            else:
                if costo == 1:
                    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
                    d = acumulado.if_04*valor+cantidad*valor
                    s = acumulado.if_04 + acumulado.ent_04+cantidad
                    if s>0:
                        costo_prom = d/s
                    else:
                        costo_prom = 0    
                    costo_prom=int(costo_prom)
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)     
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:        
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_04=entradas,ii_04=inv_inic,if_04=inv_final)
        if smes == 5:
            inv_inic = acumulado.if_04
            entradas = acumulado.ent_05
            salidas = acumulado.sal_05
            #inv_final = acumulado.if_05
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_05=salidas,ii_05=inv_inic,if_05=inv_final)
            else:
                if costo == 1:
                    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
                    d = acumulado.if_05*valor+cantidad*valor
                    s = acumulado.if_05 + acumulado.ent_05+cantidad
                    if s>0:
                        costo_prom = d/s
                    else:
                        costo_prom = 0    
                    costo_prom=int(costo_prom)
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)     
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:        
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_05=entradas,ii_05=inv_inic,if_05=inv_final)
        if smes == 6:
            inv_inic = acumulado.if_05
            entradas = acumulado.ent_06
            salidas = acumulado.sal_06
            #inv_final = acumulado.if_06
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_06=salidas,ii_06=inv_inic,if_06=inv_final)
            else:
                if costo == 1:
                    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
                    d = acumulado.if_06*valor+cantidad*valor
                    s = acumulado.if_06 + acumulado.ent_06+cantidad
                    if s>0:
                        costo_prom = d/s
                    else:
                        costo_prom = 0    
                    costo_prom=int(costo_prom)
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)     
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:        
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_06=entradas,ii_06=inv_inic,if_06=inv_final)
        if smes == 7:
            inv_inic = acumulado.if_06
            entradas = acumulado.ent_07
            salidas = acumulado.sal_07
            #inv_final = acumulado.if_07
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_07=salidas,ii_07=inv_inic,if_07=inv_final)
            else:
                if costo == 1:
                    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
                    d = acumulado.if_07*valor+cantidad*valor
                    s = acumulado.if_07 + acumulado.ent_07+cantidad
                    if s>0:
                        costo_prom = d/s
                    else:
                        costo_prom = 0    
                    costo_prom=int(costo_prom)
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)     
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:        
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_07=entradas,ii_07=inv_inic,if_07=inv_final)
        if smes == 8:
            inv_inic = acumulado.if_07
            entradas = acumulado.ent_08
            salidas = acumulado.sal_08
            #inv_final = acumulado.if_08                    
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_08=salidas,ii_08=inv_inic,if_08=inv_final)
            else:
                if costo == 1:
                    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
                    d = acumulado.if_08*valor+cantidad*valor
                    s = acumulado.if_08 + acumulado.ent_08+cantidad
                    if s>0:
                        costo_prom = d/s
                    else:
                        costo_prom = 0    
                    costo_prom=int(costo_prom)
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)     
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:        
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_08=entradas,ii_08=inv_inic,if_08=inv_final)
            
        if smes == 9:
            inv_inic = acumulado.if_08
            entradas = acumulado.ent_09
            salidas = acumulado.sal_09
            #inv_final = acumulado.if_09
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_09=salidas,ii_09=inv_inic,if_09=inv_final)
            else:
                if costo == 1:
                    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
                    d = acumulado.if_09*valor+cantidad*valor
                    s = acumulado.if_09 + acumulado.ent_09+cantidad
                    if s>0:
                        costo_prom = d/s
                    else:
                        costo_prom = 0    
                    costo_prom=int(costo_prom)
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)  
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:        
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_09=entradas,ii_09=inv_inic,if_09=inv_final)
        if smes == 10:
            inv_inic = acumulado.ii_09
            entradas = acumulado.ent_10
            salidas = acumulado.sal_10
            #inv_final = acumulado.if_10
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_10=salidas,ii_10=inv_inic,if_10=inv_final)
            else:
                if costo == 1:
                    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
                    d = acumulado.if_10*valor+cantidad*valor
                    s = acumulado.if_10 + acumulado.ent_10+cantidad
                    if s>0:
                        costo_prom = d/s
                    else:
                        costo_prom = 0    
                    costo_prom=int(costo_prom)
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)     
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:        
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_10=entradas,ii_10=inv_inic,if_10=inv_final)
        if smes == 11:
            inv_inic = acumulado.ii_10
            entradas = acumulado.ent_11
            salidas = acumulado.sal_11
            #inv_final = acumulado.if_11
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas 
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_11=salidas,ii_11=inv_inic,if_11=inv_final)
            else:
                if costo == 1:
                    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
                    d = acumulado.if_11*valor+cantidad*valor
                    s = acumulado.if_11 + acumulado.ent_11+cantidad
                    if s>0:
                        costo_prom = d/s
                    else:
                        costo_prom = 0    
                    costo_prom=int(costo_prom)
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)     
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:        
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_11=entradas,ii_11=inv_inic,if_11=inv_final)
        if smes == 12:
            inv_inic = acumulado.ii_11
            entradas = acumulado.ent_12
            salidas = acumulado.sal_12
            #inv_final = acumulado.if_12
            if topera =='salida':
                salidas = salidas+cantidad
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_12=salidas,ii_12=inv_inic,if_12=inv_final)
            else:
                if costo == 1:
                    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
                    d = acumulado.if_12*valor+cantidad*valor
                    s = acumulado.if_12 + acumulado.ent_12+cantidad
                    if s>0:
                        costo_prom = d/s
                    else:
                        costo_prom = 0    
                    costo_prom=int(costo_prom)
                    acumulado = AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(costo_prom=costo_prom)
                    MaestroItem.objects.filter(id= iditem).update(costo_prom=costo_prom)     
                entradas = entradas+cantidad
                inv_final = inv_inic+entradas-salidas
                if invinic:
                    inv_final = cantidad+entradas-salidas
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=entradas,if_01=inv_final)
                else:       
                    AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_12=entradas,ii_12=inv_inic,if_12=inv_final)

            
        x = range(1,13)    
        for i in x:
            acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)    
            if i == 1:
                inv_inic = acumulado.ii_01
                entradas = acumulado.ent_01
                salidas = acumulado.sal_01
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(if_01=inv_final)
            if i == 2:
                inv_inic = acumulado.if_01
                entradas = acumulado.ent_02
                salidas = acumulado.sal_02
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_02=inv_inic,if_02=inv_final)
            if i == 3:
                inv_inic = acumulado.if_02
                entradas = acumulado.ent_03
                salidas = acumulado.sal_03
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_03=inv_inic,if_03=inv_final)
            if i == 4:
                inv_inic = acumulado.if_03
                entradas = acumulado.ent_04
                salidas = acumulado.sal_04
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_04=inv_inic,if_04=inv_final)
            if i == 5:
                inv_inic = acumulado.if_04
                entradas = acumulado.ent_05
                salidas = acumulado.sal_05
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_05=inv_inic,if_05=inv_final)
            if i == 6:
                acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega) 
                inv_inic = acumulado.if_05
                entradas = acumulado.ent_06
                salidas = acumulado.sal_06
                inv_final = inv_inic+entradas-salidas
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_06=inv_inic,if_06=inv_final)
            if i == 7:
                acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega) 
                inv_inic = acumulado.if_06
                entradas = acumulado.ent_07
                salidas = acumulado.sal_07
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_07=inv_inic,if_07=inv_final)
            if i == 8:
                inv_inic = acumulado.if_07
                entradas = acumulado.ent_08
                salidas = acumulado.sal_08
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_08=inv_inic,if_08=inv_final)
            if i == 9:
                inv_inic = acumulado.if_08
                entradas = acumulado.ent_09
                salidas = acumulado.sal_09
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_09=inv_inic,if_09=inv_final) 
            if i == 10:
                inv_inic = acumulado.if_09
                entradas = acumulado.ent_10
                salidas = acumulado.sal_10
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_10=inv_inic,if_10=inv_final)
            if i == 11:
                inv_inic = acumulado.if_10
                entradas = acumulado.ent_11
                salidas = acumulado.sal_11
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_11=inv_inic,if_11=inv_final)
            if i == 12:
                inv_inic = acumulado.if_11
                entradas = acumulado.ent_12
                salidas = acumulado.sal_12
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_12=inv_inic,if_12=inv_final)
                #Ingrediente.objects.filter(ingrediente_id=iditem).update(cantidad_stock=inv_final)


########################################## RUTINA PROPUESTA POR GEMINI #######################################
""" def actualiza_acumulado_item(item, cantidad, mes, anio, operacion, es_inv_inicial, bodega, sucursal):
    
    Actualiza el campo correspondiente en AcumuladoItem según los parámetros.
    - item: instancia de MaestroItem o su id
    - cantidad: int
    - mes: int (1-12)
    - anio: str o int
    - operacion: 'entrada', 'salida', 'inv_inicial'
    - es_inv_inicial: bool
    - bodega: instancia de Bodega o su id
    - sucursal: instancia de Sucursal o su id

    from .models import AcumuladoItem

    # Buscar o crear el registro de acumulado
    acumulado, created = AcumuladoItem.objects.get_or_create(
        IdItem=item,
        IdBodega=bodega,
        IdSucursal=sucursal,
        anio=str(anio)
    )

    mes_str = str(mes).zfill(2)  # '01', '02', ..., '12'

    if es_inv_inicial or operacion == 'inv_inicial':
        campo = f'ii_{mes_str}'
    elif operacion == 'entrada':
        campo = f'ent_{mes_str}'
    elif operacion == 'salida':
        campo = f'sal_{mes_str}'
    else:
        raise ValueError("Operación no válida. Use 'entrada', 'salida' o 'inv_inicial'.")

    # Sumar la cantidad al campo correspondiente
    valor_actual = getattr(acumulado, campo, 0) or 0
    setattr(acumulado, campo, valor_actual + cantidad)
    acumulado.save()
    return acumulado

actualiza_acumulado_item(
    item=mi_item,           # instancia o id de MaestroItem
    cantidad=10,
    mes=5,
    anio=2025,
    operacion='entrada',    # o 'salida' o 'inv_inicial'
    es_inv_inicial=False,
    bodega=mi_bodega,       # instancia o id de Bodega
    sucursal=mi_sucursal    # instancia o id de Sucursal
) """

#####################################################################################

def PoneCerosAcumuladosInventarios(sanio,idbodega):
    items = MaestroItem.objects.filter(IdBodega_id=idbodega)
    for item in items:
        MaestroItem.objects.filter(id=item.id).update(costo_prom=0)
    x = range(1,13)    
    for i in x:
        if i == 1:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_01=0,ent_01=0,sal_01=0,if_01=0)
        if i == 2:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_02=0,ent_02=0,sal_02=0,if_02=0)
        if i == 3:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_03=0,ent_03=0,sal_03=0,if_03=0)
        if i == 4:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_04=0,ent_04=0,sal_04=0,if_04=0)
        if i == 5:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_05=0,ent_05=0,sal_05=0,if_05=0)
        if i == 6:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_06=0,ent_06=0,sal_06=0,if_06=0)
        if i == 7:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_07=0,ent_07=0,sal_07=0,if_07=0)
        if i == 8:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_08=0,ent_08=0,sal_08=0,if_08=0)
        if i == 9:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_09=0,ent_09=0,sal_09=0,if_09=0)
        if i == 10:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_10=0,ent_10=0,sal_10=0,if_10=0)
        if i == 11:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_11=0,ent_11=0,sal_11=0,if_11=0)
        if i == 12:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ii_12=0,ent_12=0,sal_12=0,if_12=0)


################################################# ACTUALIZA EL ACUMULADO EN CASCADA PROPUESTO POR GEMINI######################################################

""" def actualiza_acumulado_item_cascada(iditem, idbodega, anio):
    
    Actualiza el archivo AcumuladoItem en cascada:
    Para cada mes, el inventario inicial (ii_) será igual al inventario final (if_) del mes anterior.
    
    try:
        acumulado = AcumuladoItem.objects.get(IdItem_id=iditem, IdBodega_id=idbodega, anio=anio)
    except AcumuladoItem.DoesNotExist:
        return

    # Meses del 1 al 12
    for mes in range(2, 13):
        prev_if = getattr(acumulado, f'if_{str(mes-1).zfill(2)}', None)
        if prev_if is not None:
            setattr(acumulado, f'ii_{str(mes).zfill(2)}', prev_if)
    acumulado.save() """

def PoneCerosAcumuladosInventarios_uno(sanio,iditem):
    items = MaestroItem.objects.filter(id=iditem)
    MaestroItem.objects.filter(id=iditem).update(costo_prom=0)
    x = range(1,13)    
    for i in x:
        if i == 1:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_01=0,ent_01=0,sal_01=0,if_01=0)
        if i == 2:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_02=0,ent_02=0,sal_02=0,if_02=0)
        if i == 3:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_03=0,ent_03=0,sal_03=0,if_03=0)
        if i == 4:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_04=0,ent_04=0,sal_04=0,if_04=0)
        if i == 5:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_05=0,ent_05=0,sal_05=0,if_05=0)
        if i == 6:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_06=0,ent_06=0,sal_06=0,if_06=0)
        if i == 7:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_07=0,ent_07=0,sal_07=0,if_07=0)
        if i == 8:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_08=0,ent_08=0,sal_08=0,if_08=0)
        if i == 9:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_09=0,ent_09=0,sal_09=0,if_09=0)
        if i == 10:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_10=0,ent_10=0,sal_10=0,if_10=0)
        if i == 11:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_11=0,ent_11=0,sal_11=0,if_11=0)
        if i == 12:
            AcumuladoItem.objects.filter(anio=sanio,IdItem_id=iditem).update(ii_12=0,ent_12=0,sal_12=0,if_12=0)

def ReversaAcumuladosSalidaInventarios(iditem,cantidad,mes,anio):
    entradas = 0
    salidas = 0
    sanio = str(anio)
    smes = mes
    maestro = MaestroItem.objects.get(id=iditem)
    idbodega = maestro.IdBodega_id
    #cantidad = int(cantidad)
    if AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).exists():
        acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)

        if smes == 1:
            nueva_sal = acumulado.sal_01 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_01=nueva_sal)
        if smes == 2:
            nueva_sal = acumulado.sal_02 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_02=nueva_sal)
        if smes == 3:
            salidas_ant = acumulado.sal_03
            nueva_sal = acumulado.sal_03 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_03=nueva_sal)
        if smes == 4:
            salidas_ant = acumulado.sal_04
            nueva_sal = acumulado.sal_04 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_04=nueva_sal)
        if smes == 5:
            salidas_ant = acumulado.sal_05
            nueva_sal = acumulado.sal_05 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_05=nueva_sal)
        if smes == 6:
            salidas_ant = acumulado.sal_06
            nueva_sal = acumulado.sal_06 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_06=nueva_sal)
        if smes == 7:
            salidas_ant = acumulado.sal_07
            nueva_sal = acumulado.sal_07 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_07=nueva_sal)
            acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
        if smes == 8:
            salidas_ant = acumulado.sal_08
            nueva_sal = acumulado.sal_08 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_08=nueva_sal)
        if smes == 9:
            salidas_ant = acumulado.sal_09
            nueva_sal = acumulado.sal_09 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_09=nueva_sal)
        if smes == 10:
            salidas_ant = acumulado.sal_10
            nueva_sal = acumulado.sal_10 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_10=nueva_sal)
        if smes == 11:
            salidas_ant = acumulado.sal_11
            nueva_sal = acumulado.sal_11 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_11=nueva_sal)
        if smes == 12:
            salidas_ant = acumulado.sal_12
            nueva_sal = acumulado.sal_12 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(sal_12=nueva_sal)
            
    x = range(1,13)    
    for i in x:
        if AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).exists():
            acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)    
            if i == 1:
                inv_inic = acumulado.ii_01
                entradas = acumulado.ent_01
                salidas = acumulado.sal_01
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(if_01=inv_final)
            if i == 2:
                inv_inic = acumulado.if_01
                entradas = acumulado.ent_02
                salidas = acumulado.sal_02
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_02=inv_inic,if_02=inv_final)
            if i == 3:
                inv_inic = acumulado.if_02
                entradas = acumulado.ent_03
                salidas = acumulado.sal_03
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_03=inv_inic,if_03=inv_final)
            if i == 4:
                inv_inic = acumulado.if_03
                entradas = acumulado.ent_04
                salidas = acumulado.sal_04
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_04=inv_inic,if_04=inv_final)
            if i == 5:
                inv_inic = acumulado.if_04
                entradas = acumulado.ent_05
                salidas = acumulado.sal_05
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_05=inv_inic,if_05=inv_final)
            if i == 6:
                acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega) 
                inv_inic = acumulado.if_05
                entradas = acumulado.ent_06
                salidas = acumulado.sal_06
                inv_final = inv_inic+entradas-salidas
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_06=inv_inic,if_06=inv_final)
            if i == 7:
                acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega) 
                inv_inic = acumulado.if_06
                entradas = acumulado.ent_07
                salidas = acumulado.sal_07
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_07=inv_inic,if_07=inv_final)
            if i == 8:
                inv_inic = acumulado.if_07
                entradas = acumulado.ent_08
                salidas = acumulado.sal_08
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_08=inv_inic,if_08=inv_final)
            if i == 9:
                inv_inic = acumulado.if_08
                entradas = acumulado.ent_09
                salidas = acumulado.sal_09
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_09=inv_inic,if_09=inv_final) 
            if i == 10:
                inv_inic = acumulado.if_09
                entradas = acumulado.ent_10
                salidas = acumulado.sal_10
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_10=inv_inic,if_10=inv_final)
            if i == 11:
                inv_inic = acumulado.if_10
                entradas = acumulado.ent_11
                salidas = acumulado.sal_11
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_11=inv_inic,if_11=inv_final)
            if i == 12:
                inv_inic = acumulado.if_11
                entradas = acumulado.ent_12
                salidas = acumulado.sal_12
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_12=inv_inic,if_12=inv_final)

def ReversaAcumuladosEntradaInventarios(iditem,cantidad,mes,anio,invinic):
    entradas = 0
    salidas = 0
    #bodega_defecto = ValorDefecto.objects.get(idValor='05')
    #bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
    sanio = str(anio)
    smes = mes
    #cantidad = int(cantidad)
    item = MaestroItem.objects.get(id=iditem)
    idbodega = item.IdBodega_id
    if invinic == True:
        if AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).exists():
            acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
            nueva_ent = acumulado.ii_01 - cantidad
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_01=nueva_ent)
    else:
        if AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).exists():
            acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
            if smes == 1:
                nueva_ent = acumulado.ent_01 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_01=nueva_ent)
            if smes == 2:
                nueva_ent = acumulado.ent_02 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_02=nueva_ent)
            if smes == 3:
                nueva_ent = acumulado.ent_03 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_03=nueva_ent)
            if smes == 4:
                nueva_ent = acumulado.ent_04 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_04=nueva_ent)
            if smes == 5:
                nueva_ent = acumulado.ent_05 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_05=nueva_ent)
            if smes == 6:
                nueva_ent = acumulado.ent_06 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_06=nueva_ent)
            if smes == 7:
                nueva_ent = acumulado.ent_07 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_07=nueva_ent)
                acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)
            if smes == 8:
                nueva_ent = acumulado.ent_08 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_08=nueva_ent)
            if smes == 9:
                nueva_ent = acumulado.ent_09 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_09=nueva_ent)
            if smes == 10:
                nueva_ent = acumulado.ent_10 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_10=nueva_ent)
            if smes == 11:
                nueva_ent = acumulado.ent_11 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_11=nueva_ent)
            if smes == 12:
                nueva_ent = acumulado.ent_12 - cantidad
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ent_12=nueva_ent)
                
    x = range(1,13)    
    for i in x:
        if AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).exists():
            acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega)    
            if i == 1:
                inv_inic = acumulado.ii_01
                entradas = acumulado.ent_01
                salidas = acumulado.sal_01
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(if_01=inv_final)
            if i == 2:
                inv_inic = acumulado.if_01
                entradas = acumulado.ent_02
                salidas = acumulado.sal_02
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_02=inv_inic,if_02=inv_final)
            if i == 3:
                inv_inic = acumulado.if_02
                entradas = acumulado.ent_03
                salidas = acumulado.sal_03
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_03=inv_inic,if_03=inv_final)
            if i == 4:
                inv_inic = acumulado.if_03
                entradas = acumulado.ent_04
                salidas = acumulado.sal_04
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_04=inv_inic,if_04=inv_final)
            if i == 5:
                inv_inic = acumulado.if_04
                entradas = acumulado.ent_05
                salidas = acumulado.sal_05
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_05=inv_inic,if_05=inv_final)
            if i == 6:
                acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega) 
                inv_inic = acumulado.if_05
                entradas = acumulado.ent_06
                salidas = acumulado.sal_06
                inv_final = inv_inic+entradas-salidas
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_06=inv_inic,if_06=inv_final)
            if i == 7:
                acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega) 
                inv_inic = acumulado.if_06
                entradas = acumulado.ent_07
                salidas = acumulado.sal_07
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_07=inv_inic,if_07=inv_final)
            if i == 8:
                inv_inic = acumulado.if_07
                entradas = acumulado.ent_08
                salidas = acumulado.sal_08
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_08=inv_inic,if_08=inv_final)
            if i == 9:
                inv_inic = acumulado.if_08
                entradas = acumulado.ent_09
                salidas = acumulado.sal_09
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_09=inv_inic,if_09=inv_final) 
            if i == 10:
                inv_inic = acumulado.if_09
                entradas = acumulado.ent_10
                salidas = acumulado.sal_10
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_10=inv_inic,if_10=inv_final)
            if i == 11:
                inv_inic = acumulado.if_10
                entradas = acumulado.ent_11
                salidas = acumulado.sal_11
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_11=inv_inic,if_11=inv_final)
            if i == 12:
                inv_inic = acumulado.if_11
                entradas = acumulado.ent_12
                salidas = acumulado.sal_12
                inv_final = inv_inic+entradas-salidas  
                AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=idbodega).update(ii_12=inv_inic,if_12=inv_final)

   
def GruposInventarioListView(request):
    grupos = GruposInventarioTable(Grupo.objects.all().order_by('descripcion'))
    grupos.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'grupos':grupos}
    return render(request, 'inventarios/grupos_inventarios_lista.html', context) 

def SubGruposInventarioListView(request):
    queryset = SubGrupo.objects.all().order_by('IdGrupo__descripcion','descripcion')
    f =  SubGrupoFilter(request.GET, queryset=queryset)
    subgrupos = SubGruposInventarioTable(f.qs)
    request.session['lista_id_filtro_subgrupos'] = False
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
    request.session['lista_id_subgrupos']  = lista_id
    subgrupos.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'subgrupos':subgrupos}
    return render(request, 'inventarios/sub_grupos_inventarios_lista.html', context) 

class CreaGrupoInventarioView(LoginRequiredMixin,CreateView):
    model = Grupo
    template_name = 'inventarios/grupo_inventarios_form.html'
    form_class = GruposInventariosForm

    def get_success_url(self):
        return reverse_lazy('grupos_inventario_list')
    
class CreaSubGrupoInventarioView(LoginRequiredMixin,CreateView):
    model = SubGrupo
    template_name = 'inventarios/sub_grupo_inventarios_form.html'
    form_class = SubGruposInventariosForm

    def get_success_url(self):
        return reverse_lazy('sub_grupos_inventario_list')
        
class EditaGrupoInventarioView(LoginRequiredMixin,UpdateView):
    model = Grupo
    fields = ['idGrupo','descripcion','IdBodega']
    template_name = 'inventarios/grupo_inventarios_form.html'
    success_url = reverse_lazy('grupos_inventario_list')

class EditaSubGrupoInventarioView(LoginRequiredMixin,UpdateView):
    model = SubGrupo
    fields = ['IdGrupo','descripcion']
    template_name = 'inventarios/sub_grupo_inventarios_form.html'
    success_url = reverse_lazy('sub_grupos_inventario_list')

class BorraGrupoInventarioView(LoginRequiredMixin,DeleteView):
    model = Grupo
    success_url = reverse_lazy('grupo_inventario_list')
    template_name = 'inventarios/confirma_borrado.html'

class BorraSubGrupoInventarioView(LoginRequiredMixin,DeleteView):
    model = SubGrupo
    success_url = reverse_lazy('sub_grupos_inventario_list')
    template_name = 'inventarios/confirma_borrado.html'


def BodegasInventarioListView(request):
    bodegas = BodegasInventarioTable(Bodega.objects.all())
    bodegas.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'bodegas':bodegas}
    return render(request, 'inventarios/bodegas_inventarios_lista.html', context) 

class CreaBodegaInventarioView(LoginRequiredMixin,CreateView):
    model = Bodega
    template_name = 'inventarios/bodega_inventarios_form.html'
    form_class = BodegasInventariosForm

    def get_success_url(self):
        return reverse_lazy('bodegas_inventario_list')

    def form_valid(self, form):
        if form.is_valid():
            bodegas = form.save()
            bodegas.save()
            maestro_item = MaestroItem.objects.all()
            valor_defecto = ValorDefecto.objects.get(idValor='01')
            #sucursal = Sucursal.objects.get(idSucursal=valor_defecto.valor)
            bodega = Bodega.objects.latest('id')
            acumulado_item = AcumuladoItem() 
            for i in maestro_item:
                idbodega = bodega.id
                acumulado_item.IdItem_id = i.id
                #acumulado_item.IdSucursal_id = sucursal.id 
                acumulado_item.IdBodega_id = idbodega
                year = date.today()
                anio = year.year
                acumulado_item.anio = anio
                aa = AcumuladoItem.objects.filter(IdItem_id=i.id,IdBodega_id=idbodega,anio=anio).exists()
                if aa == False:
                    acumulado_item.save()
                    acumulado_item.id += 1
            return redirect('bodegas_inventario_list')   
            
class BorraBodegaInventarioView(LoginRequiredMixin,DeleteView):
    model = Bodega
    #success_url = reverse_lazy('bodegas_inventario_list')
    template_name = 'inventarios/confirma_borrado.html' 
    success_message = model._meta.verbose_name + "RegistroHotel Borrado"
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        bodega = Bodega.objects.get(id=pk)

        if AcumuladoItem.objects.filter(IdBodega_id=pk).exists():
            AcumuladoItem.objects.filter(IdBodega_id=pk).delete()
        return reverse('bodegas_inventario_list')

class EditaBodegaInventarioView(LoginRequiredMixin,UpdateView):
    model = Bodega
    fields = ["idBodega","descripcion","direccion","telefonos","responsable","email_bodega"]
    template_name = 'inventarios/bodega_inventarios_form.html'
    success_url = reverse_lazy('bodegas_inventario_list')       

def ItemsInventarioListView(request):
    request.session['lista_id_filtro_items'] = []
    queryset = MaestroItem.objects.all()
    idpedidos_cons=[]
    f =  MaestroItemsFilter1 (request.GET, queryset=queryset)
    for i in f.qs:
        request.session['lista_id_filtro_items'].append(i.id)
    items = ItemsInventarioTable(f.qs)
    items.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'items':items,'filter':f}
    return render(request, 'inventarios/items_inventarios_lista.html', context) 
    
def DetalleItemInventarioView(request,id):
    item = MaestroItem.objects.get(id=id)
    idbodega = item.IdBodega_id

    items1 = ItemsInventarioTable1(MaestroItem.objects.filter(id=id,IdBodega_id=idbodega))
    items2 = ItemsInventarioTable2(MaestroItem.objects.filter(id=id,IdBodega_id=idbodega))
    acumulados2 = AcumuladoItemsInventarioTable2(AcumuladoItem.objects.filter(IdItem__id=id, IdBodega_id=idbodega))
    acumulados3 = AcumuladoItemsInventarioTable3(AcumuladoItem.objects.filter(IdItem__id=id, IdBodega_id=idbodega))
    acumulados4 = AcumuladoItemsInventarioTable4(AcumuladoItem.objects.filter(IdItem__id=id, IdBodega_id=idbodega))

    context = {'items1':items1,'items2':items2,'acumulados2':acumulados2,'acumulados3':acumulados3,'acumulados4':acumulados4}
    return render(request, 'inventarios/detalle_items_inventarios_lista.html', context) 

class CreaItemInventarioView(LoginRequiredMixin,CreateView):
    model = MaestroItem
    template_name = 'inventarios/item_inventarios_form.html'
    form_class = ItemsInventariosForm

    def get_success_url(self):
        return reverse_lazy('items_inventario_list')

    def form_valid(self, form):
        if form.is_valid():
            inventario = form.save()
            inventario.save()
            maestro_item = MaestroItem.objects.all()
            #valor_defecto = ValorDefecto.objects.get(idValor='01')
            año_defecto = ValorDefecto.objects.get(idValor='06')
            año = año_defecto.valor
            #sucursal = Sucursal.objects.get(idSucursal=valor_defecto.valor)
            #bodegas = Bodega.objects.all()
            iditem = MaestroItem.objects.latest('id')
            acumulado_item = AcumuladoItem() 
            acumulado_item.IdItem_id = iditem.id
            #acumulado_item.IdSucursal_id = sucursal.id 
            item = MaestroItem.objects.get(id=iditem.id)
            idbodega = item.IdBodega_id
            acumulado_item.IdBodega_id = idbodega
            acumulado_item.anio = año
            aa = AcumuladoItem.objects.filter(IdItem_id=item.id,IdBodega_id=idbodega).exists()
            if aa == False:
                acumulado_item.save()
                #acumulado_item.id += 1
            if item.tipo_producto == 'MP':
                aa = Ingrediente.objects.filter(ingrediente_id=item.id).exists()
                if aa == False:
                    #stock = AcumuladoItem.objects.get(IdItem_id=i.id,IdBodega_id=idbodega)
                    ingrediente = Ingrediente()
                    ingrediente.ingrediente_id = item.id
                    ingrediente.descripcion = item.descripcion
                    ingrediente.unidad_medida_id = item.IdUnidadMedida_id
                    ingrediente.cantidad_stock = 0
                    ingrediente.save()
            return redirect('items_inventario_list')   
            
class BorraItemInventarioView(LoginRequiredMixin,DeleteView):
    model = MaestroItem
    #success_url = reverse_lazy('bodegas_inventario_list')
    template_name = 'inventarios/confirma_borrado.html' 
    success_message = model._meta.verbose_name + "RegistroHotel Borrado"
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        if AcumuladoItem.objects.filter(IdItem_id=pk).exists():
            AcumuladoItem.objects.filter(IdItem_id=pk).delete()
        Item = MaestroItem.objects.get(id=pk)
        if  Item.tipo_producto == 'MP':
            Ingrediente.objects.filter(ingrediente_id=Item.id).delete()
            
        return reverse('items_inventario_list')

class EditaItemInventarioView(LoginRequiredMixin,UpdateView):
    model = MaestroItem
    fields = ["IdGrupo","IdSubGrupo","descripcion","IdUnidadMedida","marca","referencia_fabrica","valor_venta","valor_compra","tipo_producto","por_iva",
              "cant_maxima","cant_minima","costo_prom","acumula","estadia","IdBodega"]
    template_name = 'inventarios/item_inventarios_form.html'
    #success_url = reverse_lazy('items_inventario_list')       
    
    def get_success_url(self):
        pk = self.kwargs["pk"]
        Ingrediente.objects.filter(ingrediente_id=pk).update(unidad_medida_id=self.object.IdUnidadMedida_id)
        return reverse("items_inventario_list")
        #success_url = reverse_lazy('items_inventario_list')
    
def MedidasInventarioListView(request):
    medidas = MedidasInventarioTable(Medida.objects.all())
    medidas.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'medidas':medidas}
    return render(request, 'inventarios/medidas_inventarios_lista.html', context) 

class CreaMedidaInventarioView(LoginRequiredMixin,CreateView):
    model = Medida
    template_name = 'inventarios/medida_inventarios_form.html'
    form_class = MedidasInventariosForm

    def get_success_url(self):
        return reverse_lazy('medidas_inventario_list')

class EditaMedidaInventarioView(LoginRequiredMixin,UpdateView):
    model = Medida
    fields = ['descripcion','abreviatura']
    template_name = 'inventarios/medida_inventarios_form.html'
    success_url = reverse_lazy('modidas_inventario_list')    


class BorraMedidaInventarioView(LoginRequiredMixin,DeleteView):
    model = Medida
    success_url = reverse_lazy('medidas_inventario_list')
    template_name = 'inventarios/confirma_borrado.html'


def EntradaAcumuladosInventarioView(request):
    if request.POST:
        form1 = MesForm(request.POST)
        form2 = AnioForm(request.POST)
        return HttpResponseRedirect('acumulado_item_inventario_list')
    else:
        form1 = AnioForm()
        form2 = MesForm()
        context = {'form1':form1,'form2':form2}
        return render(request, 'inventarios/entrada_acumulados_inventario.html', context)


def AcumuladoItemInventarioListView(request):
    idanio=request.session['idanio']
    #idmes=request.session['idmes']
    idbodega=request.session['idbodega']
    #idsucursal=request.session['idsucursal']
    anio = Anio.objects.get(id=idanio)
    items = MaestroItem.objects.filter(acumula=True)
    iditems=[]
    for i in items:
          iditems.append(i.id)
    queryset = AcumuladoItem.objects.filter(IdItem_id__in = iditems,IdBodega_id=idbodega,anio=anio.anio)
    f =  AcumuladoItemsInventarioFilter (request.GET, queryset=queryset)
    request.session['items_acumulado_filtro'] = False
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
    request.session['items_acumulado_filtro'] = lista_id    
    acumulados = AcumuladoItemsInventarioTable(f.qs)
    acumulados.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'acumulados':acumulados,'filter':f,'anio':anio}
    return render(request, 'inventarios/acumulados_items_inventarios_lista.html', context) 


def DetalleAcumuladoItemInventarioView(request,id,idbodega):
    idanio = request.session['idanio']
    anio = Anio.objects.get(id=idanio)
    acumulado = AcumuladoItem.objects.get(id=id)
    #sucursal_defecto = ValorDefecto.objects.get(idValor='01')
    #sucursal = Sucursal.objects.get(id=sucursal_defecto.id)
    item = MaestroItem.objects.get(id=acumulado.IdItem_id)
    #acumulados1 = AcumuladoItemsInventarioTable1(AcumuladoItem.objects.filter(IdSucursal__id=sucursal.id))
    acumulados1 = AcumuladoItemsInventarioTable1(AcumuladoItem.objects.filter(id=id))
    acumulados2 = AcumuladoItemsInventarioTable2(AcumuladoItem.objects.filter(IdItem__id=item.id,IdBodega_id=idbodega,anio=anio.anio))
    acumulados3 = AcumuladoItemsInventarioTable3(AcumuladoItem.objects.filter(IdItem__id=item.id,IdBodega_id=idbodega,anio=anio.anio))
    acumulados4 = AcumuladoItemsInventarioTable4(AcumuladoItem.objects.filter(IdItem__id=item.id,IdBodega_id=idbodega,anio=anio.anio))
    context = {'acumulados1':acumulados1,'acumulados2':acumulados2,'acumulados3':acumulados3,'acumulados4':acumulados4,'iditem':acumulado.IdItem_id}
    return render(request, 'inventarios/detalle_acumulados_items_inventarios_lista.html', context) 


class CreaSalidaInventarioView(LoginRequiredMixin,CreateView):
    model = Salida
    template_name = 'inventarios/salida_inventarios_form.html'
    form_class = SalidasInventariosForm

    def get_success_url(self):
        return reverse_lazy('salidas_inventario_list')

    def get_initial(self,*args,**kwargs):
        initial=super(CreaSalidaInventarioView,self).get_initial(**kwargs)
        #sucursal_defecto = ValorDefecto.objects.get(idValor='01')
        #sucursal = Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
        #initial['IdSucursal'] = sucursal.id
        #bodega_defecto = ValorDefecto.objects.get(idValor='05')
        #bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
        #initial['IdBodega'] = bodega.id
        return initial
    
    def form_valid(self, form):
        if form.is_valid():
            tipodocumento = TipoDocumentoInv.objects.get(idTipo='02')
            anumero = tipodocumento.actual +1
            snumero = str(anumero).zfill(tipodocumento.longitud)
            snumero = (tipodocumento.caracteres).strip()+snumero
            salida = form.save(commit=False)
            salida.IdUsuario_id = self.request.user.id
            salida.numero = snumero
            salida.IdTipoDocumento_id = tipodocumento.id
            salida.estado = True
            salida.save()
            TipoDocumentoInv.objects.filter(idTipo='02').update(actual = anumero)
            return redirect('salidas_inventario_list')   
        
def SalidasInventarioListView(request):
    queryset = Salida.objects.all().order_by('-fecha')
    f =  SalidasInventarioFilter (request.GET, queryset=queryset)
    lista_id = []
    request.session['filtro_idsalidas'] = False
    for n in f.qs:
        lista_id.append(n.id)
    request.session['filtro_idsalidas'] = lista_id   
    salidas = SalidasInventarioTable(f.qs)
    salidas.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'salidas':salidas,'filter':f}
    return render(request, 'inventarios/salidas_inventarios_lista.html', context) 

def DetalleSalidaInventarioView(request,id):
    salida = SalidasInventarioTable(Salida.objects.filter(id=id))
    detalle_salida = SalidasInventarioDetalleTable(SalidaDetalle.objects.filter(IdSalida_id=id))
    request.session['filtro_idsalidas'] = False
    lista_id = []
    lista_id.append(id)
    request.session['filtro_idsalidas'] = lista_id
    context = {'salida':salida,'detalle_salida':detalle_salida}
    return render(request, 'inventarios/detalle_salida_inventarios.html', context) 

def VerificaDetalleSalidaInventarioView(request,id):
    aa = SalidaDetalle.objects.filter(IdSalida_id=id).exists()
    if aa:
        return redirect('detalle_salida_inventario',id)
    else:
        request.session['idsalida'] = id
        return redirect('selecciona_item_salida_inventarios',id)   

def CreaDetalleSalidaInventarioView(request,id):
    request.session['idsalida'] = id
    return redirect('selecciona_item_salida_inventarios',id)


def SeleccionaItemSalidaInventariosView(request,id):
    request.session['idsalida'] = id
    return redirect(reverse('filtra_item_salida_inventarios'))

class FiltraItemSalidaInventariosView(SingleTableMixin, FilterView):
    table_class = ItemsListaTable1
    model = MaestroItem
    template_name = "inventarios/items_salida_inventario_filter.html"
    filterset_class = MaestroItemsFilter
    paginate_by = 8

def FiltraSubGrupoPorGrupoInventarioView(request):
    idgrupo = request.GET.get('idgrupo', None)
    subgrupos = SubGrupo.objects.filter(IdGrupo_id=idgrupo).values('descripcion', 'id')
    return HttpResponse(json.dumps( list(subgrupos)), content_type='application/json')

""" def ItemPedidoSalida(request):
    request.session['sel_item']= True
    a = request.session['sel_item']
    iditem = request.GET.get('id', None)
    cantidad = request.GET.get('cantidad', None)
    idsalida = request.session['idsalida']
    AdicionaItemSalida(iditem,cantidad,idsalida)
    #MaestroItem.objects.filter(iditem=iditem).
    #PoneAcumuladosInventario(iditem,cantidad)
    data={'a':0}
    return JsonResponse(data) """

def GuardaIdSalida(request):
    idsalida = request.GET.get('id', None)
    detalle_salida = SalidaDetalle.objects.get(id=idsalida)
    request.session['id_item_anterior'] = detalle_salida.IdItem_id 
    request.session['id_salida_detalle'] = idsalida
    request.session['cantidad_anterior'] = detalle_salida.cantidad
    request.session['numero_salida'] = detalle_salida.numero
    data={'a':0}
    return JsonResponse(data)

def GuardaItemSalida(request):
    request.session['sel_item']= True
    a = request.session['sel_item']
    iditem = request.GET.get('id', None)
    cantidad = request.GET.get('cantidad', None)
    idsalida = request.session['idsalida']
    AdicionaItemSalida(iditem,cantidad,idsalida)
    data={'a':0}
    return JsonResponse(data)
    
def AdicionaItemSalida(iditem,cantidad,idsalida):
    detalle_salida = SalidaDetalle()
    item = MaestroItem.objects.get(id=iditem)
    idbodega = item.IdBodega_id
    salida = Salida.objects.get(id=idsalida)        
    idtipodoc = TipoDocumentoInv.objects.get(idTipo='02')
    detalle_salida.numero = salida.numero
    detalle_salida.IdTipoDocumento_id = idtipodoc.id
    detalle_salida.IdSalida_id = salida.id
    detalle_salida.IdItem_id = iditem
    detalle_salida.IdBodega_id = idbodega
    detalle_salida.estado = 1
    detalle_salida.valor = item.valor_venta
    detalle_salida.cantidad = cantidad
    detalle_salida.valor_total = item.valor_venta*int(float(cantidad))
    detalle_salida.save()
    #InterfaseSalidaInventariosCuerpo(salida.numero,iditem,cantidad,item.valor_venta,item.valor_venta*int(float(cantidad)))
    salida_detalle_regs = SalidaDetalle.objects.filter(IdSalida_id=idsalida)
    total=0
    items = 0
    year = salida.fecha
    anio = year.year
    mes = year.month
    invinic = False
    for sal in salida_detalle_regs:
        total = total + sal.valor*sal.cantidad
        items = items + 1
        item = MaestroItem.objects.get(id=sal.IdItem_id)
        SalidaDetalle.objects.filter(id=sal.id).update(valor_total=sal.valor*sal.cantidad)
    ActualizaAcumuladosInventarios(sal.IdItem_id,sal.cantidad,0,mes,anio,'salida',0,invinic)
    Salida.objects.filter(numero=salida.numero).update(valor=total)    
    
def DireccionaInventarios(request,id):
    if id == 1:
        idsalida = request.session['idsalida']
        return redirect('detalle_salida_inventario',idsalida)
    
    if id == 2:
        identrada=request.session['identrada']
        #entrada_detalle = EntradaDetalle.objects.get(id=identrada_detalle)
        #entrada = Entrada.objects.get(id=entrada_detalle.IdEntrada_id)
        return redirect('entradas_inventario_list')
    
    if id == 3:
        identrada=request.session['identrada']
        #entrada_detalle = EntradaDetalle.objects.get(id=identrada_detalle)
        #entrada = Entrada.objects.get(id=entrada_detalle.IdEntrada_id)
        return redirect('detalle_entrada_inventario',identrada)
    
class EditaSalidaInventarioView(LoginRequiredMixin,UpdateView):
    model = Salida
    fields = ['fecha','detalle']
    template_name = 'inventarios/salida_inventarios_form.html'
    success_url = reverse_lazy('salidas_inventario_list')

def ValidaEditarSalidaInventarioView(request,id):
    salida = Salida.objects.get(id=id)
    tipodocumento = TipoDocumentoInv.objects.get(id=salida.IdTipoDocumento_id)
    if tipodocumento.idTipo == '04' :
        mensaje1 = "Esta Salida se originó en el Pedido de Caja : "
        mensaje2 = salida.pedido_caja+" "
        mensaje3 = "por lo tanto no se puede modificar "
        parametro = 1  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_editar_salidas_inventarios.html', context)      
    else:
        return reverse_lazy('edita_salida_inventario', kwargs={'pk':id})
        #return redirect('edita_salida_inventario',pk=id)

class SeleccionaCajaReciboCajaConsolidadoView(TemplateView):
    template_name = "caja/selecciona_caja_cierre_consolidado.html"   

class EditaDetalleSalidaInventarioView(LoginRequiredMixin,UpdateView):
    model = SalidaDetalle
    fields = ['IdItem','valor','cantidad']
    template_name = 'inventarios/detalle_salida_inventarios_form.html'
    id = 1
    success_url = reverse_lazy('direcciona_inventarios',args=[id])

    def get_success_url(self, *args, **kwargs):
        id_item_anterior = self.request.session['id_item_anterior']
        id_salida_detalle = self.request.session['id_salida_detalle']
        cantidad_anterior = self.request.session['cantidad_anterior']
        salida_detalle = SalidaDetalle.objects.get(id=id_salida_detalle)
        salida = Salida.objects.get(numero=salida_detalle.numero)
        year = salida.fecha
        anio = year.year
        mes = year.month
        item = MaestroItem.objects.get(id=salida_detalle.IdItem_id)
        invinic = False
        ReversaAcumuladosSalidaInventarios(id_item_anterior,cantidad_anterior,mes,anio)
        id_item_actual = self.object.pk
        salida_detalle = SalidaDetalle.objects.get(id=id_salida_detalle)
        id_item_actual = salida_detalle.IdItem_id
        valor_total = salida_detalle.valor*salida_detalle.cantidad
        if salida.IdTipoDocumento_id == 5:
            invinic = True
        else:
            invinic = False    
        ActualizaAcumuladosInventarios(id_item_actual,salida_detalle.cantidad,0,mes,anio,'salida',0,invinic)
        SalidaDetalle.objects.filter(id=id_salida_detalle).update(valor_total=valor_total)
        return reverse_lazy('detalle_salida_inventario', kwargs={'id':salida.id})        

def ValidaEditarDetalleSalidaInventarioView(request,id):
    detalle_salida = SalidaDetalle.objects.get(id=id)
    salida = Salida.objects.get(id=detalle_salida.IdSalida_id)
    tipodocumento = TipoDocumentoInv.objects.get(id=detalle_salida.IdTipoDocumento_id)
    if tipodocumento.idTipo == '04' :
        mensaje1 = "Esta Salida se originó en el Pedido de Caja : "
        mensaje2 = salida.pedido_caja+" "
        mensaje3 = "por lo tanto no se puede modificar "
        parametro = 1  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_editar_salidas_inventarios.html', context)      
    else:
        return redirect('edita_salida_detalle_inventario',pk=id)

def ValidaCreaDetalleSalidaInventarioView(request,id):
    detalle_salida = SalidaDetalle.objects.get(id=id)
    salida = Salida.objects.get(id=detalle_salida.IdSalida_id)
    tipodocumento = TipoDocumentoInv.objects.get(id=detalle_salida.IdTipoDocumento_id)
    if tipodocumento.idTipo == '04' :
        mensaje1 = "Esta Salida se originó en el Pedido de Caja : "
        mensaje2 = salida.pedido_caja+" "
        mensaje3 = "por lo tanto no se puede modificar "
        parametro = 1  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_editar_salidas_inventarios.html', context)      
    else:
        return redirect('edita_salida_detalle_inventario',pk=id)
    
def BuscaItemInventarioView(request):
    iditem = request.GET.get('iditem', None)
    item = MaestroItem.objects.get(id=iditem)
    data = {'valor_venta':item.valor_venta}
    return JsonResponse(data)

class BorraSalidaInventarioView(LoginRequiredMixin,DeleteView):
    model = Salida
    success_url = reverse_lazy('salidas_inventario_list')
    template_name = 'inventarios/confirma_borrado.html'

def BorraSalidaPorVentaInventarioView(request,id):
    if id == 1:
        idsalida = request.session['idsalida']
        salida = Salida.objects.get(id=idsalida)
        SalidaDetalle.objects.filter(IdSalida_id=idsalida).delete()
        Salida.objects.filter(id=idsalida).delete()
    return redirect('salidas_inventario_list')

def ValidaBorrarSalidaInventarioView(request,id):
    salida = Salida.objects.get(id=id)
    tipodocumento = TipoDocumentoInv.objects.get(id=salida.IdTipoDocumento_id)
    if tipodocumento.idTipo == '04' :
        if PedidoCaja.objects.filter(numero=salida.pedido_caja).exists():
            mensaje1 = "Esta Salida se originó en el Pedido de Caja : "
            mensaje2 = salida.pedido_caja+" "
            mensaje3 = "Debe borrar primero el pedido de caja! "
            parametro = 1  
            context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
            return render(request, 'inventarios/mensaje_editar_salidas_inventarios.html', context)
        else:
            request.session['idsalida'] = salida.id
            mensaje1 = "El registro será borrado !"
            mensaje2 = " "
            mensaje3 = ""
            parametro = 1  
            context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
            return render(request, 'inventarios/mensaje_confirma_borrado_salida_inventario.html', context)          
    else:
        if SalidaDetalle.objects.filter(IdSalida_id=id).exists():
            mensaje1 = "Esta Salida tiene items en el detalle, "
            mensaje2 = " debe borrarlos primero."
            mensaje3 = ""
            parametro = 1  
            context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
            return render(request, 'inventarios/mensaje_editar_salidas_inventarios.html', context)      
        else:
            return redirect('borra_salida_inventario',pk=id)
    
def ValidaBorrarDetalleSalidaInventarioView(request,id):
    detalle_salida = SalidaDetalle.objects.get(id=id)
    salida = Salida.objects.get(id=detalle_salida.IdSalida_id)
    tipodocumento = TipoDocumentoInv.objects.get(id=detalle_salida.IdTipoDocumento_id)
    if tipodocumento.idTipo == '04' :
        mensaje1 = "Esta Salida se originó en el Pedido de Caja : "
        mensaje2 = salida.pedido_caja+" "
        mensaje3 = "por lo tanto no se puede borrar "
        parametro = 1  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_editar_salidas_inventarios.html', context)       
    else:
        mensaje1 = "El registro será borrado !"
        mensaje2 = " "
        mensaje3 = ""
        parametro = 1  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_confirma_borrado_detalle_inventario.html', context)    
    
""" def ValidaBorrarDetalleSalidaInventarioView(request,id):
    mensaje1 = "El registro será borrado !"
    mensaje2 = " "
    mensaje3 = ""
    parametro = 1  
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
    return render(request, 'inventarios/mensaje_confirma_borrado_detalle_inventario.html', context)      
     """
        
def BorraSalidaDetalleInventarioView(request,id):
    id_item_anterior = request.session['id_item_anterior']
    id_salida_detalle = request.session['id_salida_detalle']
    cantidad_anterior = request.session['cantidad_anterior']
    numero_salida = request.session['numero_salida']
    salida = Salida.objects.get(numero=numero_salida)
    year = salida.fecha
    anio = year.year
    mes = year.month
    item = MaestroItem.objects.get(id=id_item_anterior)
    if id == 1:
        ReversaAcumuladosSalidaInventarios(id_item_anterior,cantidad_anterior,mes,anio)
        SalidaDetalle.objects.filter(id=id_salida_detalle).delete()

    return redirect('detalle_salida_inventario', salida.id)

""" class BorraSalidaDetalleInventarioView(LoginRequiredMixin,DeleteView):
    model = SalidaDetalle
    #success_url = reverse_lazy('detalle_salida_inventario',id)
    template_name = 'inventarios/confirma_borrado.html'

    def get_success_url(self, *args, **kwargs):
        id_item_anterior = self.request.session['id_item_anterior']
        id_salida_detalle = self.request.session['id_salida_detalle']
        cantidad_anterior = self.request.session['cantidad_anterior']
        salida_detalle = SalidaDetalle.objects.get(id=id_salida_detalle)
        salida = Salida.objects.get(numero=salida_detalle.numero)
        year = salida.fecha
        anio = year.year
        mes = year.month
        print('Cantidad Anterior :',cantidad_anterior)
        print('Id Item Anter.:',id_item_anterior)
        ReversaAcumuladosSalidaInventarios(id_item_anterior,cantidad_anterior,mes,anio)
        return reverse_lazy('detalle_salida_inventario', kwargs={'id':salida.id})  """ 
    
    
""" def ValidaBorrarDetalleSalidaInventarioView(request,id):
    detalle_salida = SalidaDetalle.objects.get(id=id)
    salida = Salida.objects.get(id=detalle_salida.IdSalida_id)
    if detalle_salida.IdTipoDocumento_id == 4 :
        mensaje1 = "Esta Salida se originó en el Pedido de Caja : "
        mensaje2 = salida.pedido_caja+" "
        mensaje3 = "por lo tanto no se puede borrar "
        parametro = 1  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_editar_salida_inventarios.html', context)      
    else:
        return redirect('borra_salida_detalle_inventario',pk=id) """

def EntradaRecuperacionSaldosInventarioView(request):
    if request.POST:
        form1 = MesForm(request.POST)
        form2 = AnioForm(request.POST)
        return HttpResponseRedirect('inventario_fisico')
    else:
        form1 = AnioForm()
        form2 = MesForm()
        context = {'form1':form1,'form2':form2}
        return render(request, 'inventarios/entrada_recuperacion_saldos.html', context)

""" def EntradaRecuperacionSaldosInventarioUnoView(request):
    if request.POST:
        form1 = MesForm(request.POST)
        form2 = AnioForm(request.POST)
        return HttpResponseRedirect('inventario_fisico')
    else:
        id = request.session['iditem']
        form1 = AnioForm()
        form2 = MesForm()
        context = {'form1':form1,'form2':form2}
        return render(request, 'inventarios/entrada_recuperacion_saldos_uno.html', context) """

def RecuperacionSaldosInventarioUnoView(request):
    iditem = request.session['iditem']
    idacumulado = request.session['idacumulado']
    idanio=request.session['idanio']
    idbodega=request.session['idbodega']
    anio = Anio.objects.get(id=idanio)
    PoneCerosAcumuladosInventarios_uno(anio.anio,iditem)
    RecuperaSaldosInventariosSalida_uno(anio.anio,iditem)
    RecuperaSaldosInventariosEntrada_uno(anio.anio,iditem)
    mensaje1 = "Proceso Terminado : "
    mensaje2 = ""
    mensaje3 = ""
    parametro = 5
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro,'idacumulado':idacumulado,'idbodega':idbodega}
    return render(request, 'inventarios/mensaje_proceso_terminado.html', context)  


def RecuperacionSaldosInventarioView(request):
    #iditem = request.session['iditem']
    #idacumulado = request.session['idacumulado']
    idanio=request.session['idanio']
    idbodega=request.session['idbodega']
    anio = Anio.objects.get(id=idanio)
    PoneCerosAcumuladosInventarios(anio.anio,idbodega)
    RecuperaSaldosInventariosSalida(anio.anio,idbodega)
    RecuperaSaldosInventariosEntrada(anio.anio,idbodega)
    mensaje1 = "Proceso Terminado : "
    mensaje2 = ""
    mensaje3 = ""
    parametro = 1
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro,'idbodega':idbodega}
    return render(request, 'inventarios/mensaje_proceso_terminado.html', context)  
    
def RecuperaSaldosInventariosSalida(anio,idbodega):    
    # Borra los documentos de salida por pedido de inventarios
    #bodega_defecto = ValorDefecto.objects.get(idValor='05')
    #bodega =Bodega.objects.get(idBodega=bodega_defecto.valor)
    #año_defecto = ValorDefecto.objects.get(idValor='06')
    #anio = str(año_defecto.valor)
    salidas = Salida.objects.filter(anio = anio)
    for sale in salidas:
        year = sale.fecha
        anio = year.year
        mes = year.month
        salida_detalle = SalidaDetalle.objects.filter(IdSalida_id=sale.id)
        invinic = False
        for sal in salida_detalle:
            item = MaestroItem.objects.get(id=sal.IdItem_id)
            ActualizaAcumuladosInventarios(sal.IdItem_id,sal.cantidad,0,mes,anio,'salida',0,invinic)

def RecuperaSaldosInventariosSalida_uno(anio,iditem):    
    # Borra los documentos de salida por pedido de inventarios
    #bodega_defecto = ValorDefecto.objects.get(idValor='05')
    #bodega =Bodega.objects.get(idBodega=bodega_defecto.valor)
    #año_defecto = ValorDefecto.objects.get(idValor='06')
    #anio = str(año_defecto.valor)
    salidas = Salida.objects.filter(anio = anio)
    for sale in salidas:
        year = sale.fecha
        anio = year.year
        mes = year.month
        salida_detalle = SalidaDetalle.objects.filter(IdSalida_id=sale.id, IdItem_id=iditem)
        invinic = False
        for sal in salida_detalle:
            ActualizaAcumuladosInventarios(sal.IdItem_id,sal.cantidad,0,mes,anio,'salida',0,invinic)

def RecuperaSaldosInventariosEntrada(anio,idbodega):    
    # Borra los documentos de salida por pedido de inventarios
    #bodega_defecto = ValorDefecto.objects.get(idValor='05')
    #bodega =Bodega.objects.get(idBodega=bodega_defecto.valor)
    #año_defecto = ValorDefecto.objects.get(idValor='06')
    #anio = str(año_defecto.valor)
    #entradas = Entrada.objects.filter(fecha.year=anio)
    entradas = Entrada.objects.filter(anio = anio)
    for entra in entradas:
        year = entra.fecha
        anio = year.year
        mes = year.month
        entrada_detalle = EntradaDetalle.objects.filter(IdEntrada_id=entra.id)
        idtipodocumento = TipoDocumentoInv.objects.get(id=entra.IdTipoDocumento_id)
        for ent in entrada_detalle:
            item = MaestroItem.objects.get(id=ent.IdItem_id)
            if idtipodocumento.idTipo == '06':
                costo = 1
            else:
                costo = 0
            if idtipodocumento.idTipo == '05':
                invinic = True
            else:
                invinic = False            
            ActualizaAcumuladosInventarios(ent.IdItem_id,ent.cantidad,ent.valor,mes,anio,'entrada',costo,invinic)

def RecuperaSaldosInventariosEntrada_uno(anio,iditem):    
    # Borra los documentos de salida por pedido de inventarios
    #bodega_defecto = ValorDefecto.objects.get(idValor='05')
    #bodega =Bodega.objects.get(idBodega=bodega_defecto.valor)
    #año_defecto = ValorDefecto.objects.get(idValor='06')
    #anio = str(año_defecto.valor)
    #entradas = Entrada.objects.filter(fecha.year=anio)
    entradas = Entrada.objects.filter(anio = anio)
    #print(entradas)
    for entra in entradas:
        year = entra.fecha
        anio = year.year
        mes = year.month
        entrada_detalle = EntradaDetalle.objects.filter(numero=entra.numero,IdItem_id=iditem)
        print(entrada_detalle)
        idtipodocumento = TipoDocumentoInv.objects.get(id=entra.IdTipoDocumento_id)
        for ent in entrada_detalle:
            #item = MaestroItem.objects.get(id=ent.IdItem_id)
            print(ent.numero)
            if idtipodocumento.idTipo == '06':
                costo = 1
            else:
                costo = 0
            if idtipodocumento.idTipo == '05':
                invinic = True
            else:
                invinic = False            
            ActualizaAcumuladosInventarios(ent.IdItem_id,ent.cantidad,ent.valor,mes,anio,'entrada',costo,invinic)

class CreaEntradaInventarioView(LoginRequiredMixin,CreateView):
    model = Entrada
    template_name = 'inventarios/entrada_inventarios_form.html'
    form_class = EntradasInventariosForm

    def get_success_url(self):
        return reverse_lazy('entradas_inventario_list')

    def get_initial(self,*args,**kwargs):
        initial=super(CreaEntradaInventarioView,self).get_initial(**kwargs)
        #sucursal_defecto = ValorDefecto.objects.get(idValor='01')
        #sucursal = Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
        #initial['IdSucursal'] = sucursal.id
        #bodega_defecto = ValorDefecto.objects.get(idValor='05')
        #bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
        #initial['IdBodega'] = bodega.id
        #initial['fecha'] = date.today()
        return initial
    
    def form_valid(self, form):
        if form.is_valid():
            #tipodocumento = TipoDocumentoInv.objects.get(id=1)
            idtipodocumento = form.instance.IdTipoDocumento
            tipodocumento = TipoDocumentoInv.objects.get(id=idtipodocumento.id)
            anumero = tipodocumento.actual +1
            snumero = str(anumero).zfill(tipodocumento.longitud)
            snumero = (tipodocumento.caracteres).strip()+snumero
            entrada = form.save(commit=False)
            entrada.IdUsuario_id = self.request.user.id
            entrada.numero = snumero
            entrada.IdTipoDocumento_id = tipodocumento.id
            entrada.estado = True
            #entrada.anio = str(form.fecha.year)
            entrada.save()
            entrada = Entrada.objects.get(numero=snumero)
            Entrada.objects.filter(numero=snumero).update(anio=str(entrada.fecha.year))
            TipoDocumentoInv.objects.filter(id=idtipodocumento.id).update(actual = anumero)
            return redirect('entradas_inventario_list')   
                    
def EntradasInventarioListView(request):
    queryset = Entrada.objects.all().order_by('-fecha')
    f =  EntradasInventarioFilter (request.GET, queryset=queryset)
    lista_id = []
    request.session['filtro_identradas'] = False
    for n in f.qs:
        lista_id.append(n.id)
    request.session['filtro_identradas'] = lista_id    
    entradas = EntradasInventarioTable(f.qs)
    entradas.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'entradas':entradas,'filter':f}
    return render(request, 'inventarios/entradas_inventarios_lista.html', context) 

def DetalleEntradaInventarioView(request,id):
    entrada = EntradasInventarioTable(Entrada.objects.filter(id=id))
    detalle_entrada = EntradasInventarioDetalleTable(EntradaDetalle.objects.filter(IdEntrada_id=id))
    lista_id = []
    lista_id.append(id)
    request.session['filtro_identradas'] = lista_id
    context = {'entrada':entrada,'detalle_entrada':detalle_entrada}
    return render(request, 'inventarios/detalle_entrada_inventarios.html', context) 

def EditaEntradaInventarioView(request,id):
    instancia = get_object_or_404(Entrada, pk=id)
    form = EntradasInventariosForm(request.POST or None, instance = instancia)
    if form.is_valid():
        instancia = form.save(commit=False)
        instancia.save()
        return redirect('entradas_inventario_list')
    else:
        form = EntradasInventariosForm(instance=instancia)
    return render(request, 'inventarios/entrada_inventarios_form.html', {'form':form})

def ValidaEditarEntradaInventarioView(request,id):
    entrada = Entrada.objects.get(id=id)
    idtipodocumento = TipoDocumentoInv.objects.get(id=entrada.IdTipoDocumento_id)
    if  idtipodocumento.idTipo == '06' :
        mensaje1 = "Esta Entrada se originó en un Despacho : "
        mensaje2 = entrada.despacho+" "
        mensaje3 = ", debe modificar el despacho"
        parametro = 1  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_editar_entradas_inventarios.html', context)      
    else:
        return redirect('edita_entrada_inventario',id)
    
def ValidaEditarDetalleEntradaInventarioView(request,id):
    detalle_entrada = EntradaDetalle.objects.get(id=id)
    entrada = Entrada.objects.get(numero=detalle_entrada.numero)
    idtipodocumento = TipoDocumentoInv.objects.get(id=detalle_entrada.IdTipoDocumento_id)
    if  idtipodocumento.idTipo == '06' :
        mensaje1 = "Esta Entrada se originó en en un Despacho : "
        mensaje2 = " "+entrada.despacho+" "
        mensaje3 = ",debe modificar el despacho "
        parametro = 1  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_editar_entradas_inventarios.html', context)      
    else:
        return redirect('edita_entrada_detalle_inventario',id)
       
class EditaEntradaDetalleInventarioView(LoginRequiredMixin,UpdateView):
    model = EntradaDetalle
    fields = ['IdItem','valor','cantidad']
    template_name = 'inventarios/detalle_entrada_inventarios_form.html'
    id = 1
    #success_url = reverse_lazy('direcciona_inventarios',args=[id])    

    def get_success_url(self, *args, **kwargs):
        id_item_anterior = self.request.session['id_item_anterior']
        id_entrada_detalle = self.request.session['id_entrada_detalle']
        cantidad_anterior = self.request.session['cantidad_anterior']
        entrada_detalle = EntradaDetalle.objects.get(id=id_entrada_detalle)
        entrada = Entrada.objects.get(numero=entrada_detalle.numero)
        year = entrada.fecha
        anio = year.year
        mes = year.month
        idtipodocumento = TipoDocumentoInv.objects.get(id=entrada_detalle.IdTipoDocumento_id)
        item = MaestroItem.objects.get(id=id_item_anterior)
        if idtipodocumento.idTipo == '05':
            invinic=True
        else:    
            invinic=False
        ReversaAcumuladosEntradaInventarios(id_item_anterior,cantidad_anterior,mes,anio,invinic)
        id_item_actual = self.object.pk
        entrada_detalle = EntradaDetalle.objects.get(id=id_entrada_detalle)
        id_item_actual = entrada_detalle.IdItem_id
        valor_total = entrada_detalle.valor*entrada_detalle.cantidad
        
        if idtipodocumento.idTipo == '06'or idtipodocumento.idTipo == '05':
            costo = 1
        else:
            costo = 0 
        item = MaestroItem.objects.get(id=id_item_actual)    
        ActualizaAcumuladosInventarios(id_item_actual,entrada_detalle.cantidad,entrada_detalle.valor,mes,anio,'entrada',costo,invinic)
        entrada_detalle = EntradaDetalle.objects.get(id=id_entrada_detalle)
        EntradaDetalle.objects.filter(id=id_entrada_detalle).update(valor_total=valor_total)
        #entrada = Entrada.objects.get(id=entrada_detalle.IdEntrada_id)
        total = EntradaDetalle.objects.filter(numero=entrada_detalle.numero).aggregate(Sum('valor_total'))['valor_total__sum']  
        Entrada.objects.filter(id=entrada_detalle.IdEntrada_id).update(valor=total)
        return reverse_lazy('detalle_entrada_inventario', kwargs={'id':entrada.id})     

def ValidaBorrarEntradaInventarioView(request,id):
    entrada = Entrada.objects.get(id=id)
    idtipodocumento = TipoDocumentoInv.objects.get(id=entrada.IdTipoDocumento_id)
    if idtipodocumento.idTipo == '06':
        despacho = entrada.despacho
        if Despacho.objects.filter(numero=despacho).exists:
            mensaje1 = "Esta Entrada se originó en un Despacho : "
            mensaje2 = entrada.despacho+" "
            mensaje3 = "debe borrar el despacho "
            parametro = 1  
            context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
            return render(request, 'inventarios/mensaje_editar_entradas_inventarios.html', context)
        else:
            return redirect('borra_entrada_inventario',pk=id)      
    else:
        if EntradaDetalle.objects.filter(IdEntrada_id=id).exists():
            mensaje1 = "Esta Entrada tiene items en el detalle, "
            mensaje2 = " debe borrarlos primero."
            mensaje3 = ""
            parametro = 1  
            context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
            return render(request, 'inventarios/mensaje_editar_entradas_inventarios.html', context)      
        else:
            return redirect('borra_entrada_inventario',pk=id)
            
class BorraEntradaInventarioView(LoginRequiredMixin,DeleteView):
    model = Entrada
    success_url = reverse_lazy('entradas_inventario_list')
    template_name = 'inventarios/confirma_borrado.html'


def ValidaBorrarDetalleEntradaInventarioView(request,id):
    detalle_entrada = EntradaDetalle.objects.get(id=id)
    entrada = Entrada.objects.get(id=detalle_entrada.IdEntrada_id)
    idtipodocumento = TipoDocumentoInv.objects.get(id=entrada.IdTipoDocumento_id)
    if idtipodocumento.idTipo == '06':
        mensaje1 = "Esta Entrada se originó en un Despacho : "
        mensaje2 = entrada.despacho+" "
        mensaje3 = "debe borrar el despacho "
        parametro = 2 
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_editar_entradas_inventarios.html', context)      
    else:
        mensaje1 = "El registro será borrado !"
        mensaje2 = " "
        mensaje3 = ""
        parametro = 2
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_confirma_borrado_detalle_inventario.html', context)    
           
""" class BorraEntradaDetalleInventarioView(LoginRequiredMixin,DeleteView):
    model = EntradaDetalle
    #success_url = reverse_lazy('detalle_salida_inventario',id)
    template_name = 'inventarios/confirma_borrado.html'

    def get_success_url(self, *args, **kwargs):
        id_item_anterior = self.request.session['id_item_anterior']
        id_entrada_detalle = self.request.session['id_entrada_detalle']
        cantidad_anterior = self.request.session['cantidad_anterior']
        numero_entrada = self.request.session['numero_entrada']
        entrada = Entrada.objects.get(numero=numero_entrada)
        year = entrada.fecha
        anio = year.year
        mes = year.month
        ReversaAcumuladosEntradaInventarios(id_item_anterior,cantidad_anterior,mes,anio)
        return reverse_lazy('detalle_entrada_inventario', kwargs={'id':entrada.id})   """

""" def ValidaBorrarDetalleEntradaInventarioView(request,id):
    mensaje1 = "El registro será borrado !"
    mensaje2 = " "
    mensaje3 = ""
    parametro = 1  
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
    return render(request, 'inventarios/mensaje_confirma_borrado_detalle_inventario.html', context)       """
    
        
def BorraEntradaDetalleInventarioView(request,id):
    id_item_anterior = request.session['id_item_anterior']
    id_entrada_detalle = request.session['id_entrada_detalle']
    cantidad_anterior = request.session['cantidad_anterior']
    #numero_entrada = request.session['numero_entrada']
    bodega_defecto = ValorDefecto.objects.get(idValor='05')
    bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
    detalle_entrada = EntradaDetalle.objects.get(id=id_entrada_detalle)
    entrada = Entrada.objects.get(numero=detalle_entrada.numero)
    year = entrada.fecha
    anio = year.year
    mes = year.month
    idtipodoc = detalle_entrada.IdTipoDocumento_id
    tipodoc = TipoDocumentoInv.objects.get(id=idtipodoc)
    if tipodoc.idTipo == '05':
        invinic = True
    else:
        invinic = False     
    if id == 1:
        item = MaestroItem.objects.get(id=id_item_anterior)
        ReversaAcumuladosEntradaInventarios(id_item_anterior,cantidad_anterior,mes,anio,invinic)
        EntradaDetalle.objects.filter(id=id_entrada_detalle).delete()

    return redirect('detalle_entrada_inventario', entrada.id)

def VerificaDetalleEntradaInventarioView(request,id):
    aa = EntradaDetalle.objects.filter(IdEntrada_id=id).exists()
    if aa:
        return redirect('detalle_entrada_inventario',id)
    else:
        request.session['identrada'] = id
        return redirect('selecciona_item_entrada_inventarios',id) 
    
def SeleccionaItemEntradaInventariosView(request,id):
    request.session['identrada'] = id
    return redirect('filtra_item_entrada_inventarios')    

class FiltraItemEntradaInventariosView(SingleTableMixin, FilterView):
    table_class = ItemsListaTable
    model = MaestroItem
    template_name = "inventarios/items_entrada_inventario_filter.html"
    filterset_class = MaestroItemsFilter
    paginate_by = 8

def AdicionaItemEntrada(iditem,cantidad,identrada,valor):
    entrada = Entrada.objects.get(id=identrada)
    #idtipodoc = entrada.IdTipoDocumento_id
    #tipodoc = TipoDocumentoInv.objects.get(id=idtipodoc)
    valor = int(valor)
    detalle_entrada = EntradaDetalle()
    item = MaestroItem.objects.get(id=iditem)
    idbodega = item.IdBodega_id    
    detalle_entrada.numero = entrada.numero
    detalle_entrada.IdTipoDocumento_id = entrada.IdTipoDocumento_id
    detalle_entrada.IdEntrada_id = entrada.id
    detalle_entrada.IdItem_id = iditem
    detalle_entrada.IdBodega_id = idbodega
    detalle_entrada.estado = 1
    detalle_entrada.valor = valor
    detalle_entrada.cantidad = cantidad
    detalle_entrada.valor_total = item.valor_venta*int(cantidad)
    detalle_entrada.save()
    #InterfaseSalidaInventariosCuerpo(salida.numero,iditem,cantidad,item.valor_venta,item.valor_venta*int(float(cantidad)))
    entrada_detalle_regs = EntradaDetalle.objects.filter(IdEntrada_id=identrada)
    total=0
    items = 0
    year = entrada.fecha
    anio = year.year
    mes = year.month
    for ent in entrada_detalle_regs:
        total = total + ent.valor*ent.cantidad
        items = items + 1
        EntradaDetalle.objects.filter(id=ent.id).update(valor_total=ent.valor*ent.cantidad)
        total = EntradaDetalle.objects.filter(numero=entrada.numero).aggregate(Sum('valor_total'))['valor_total__sum']  
        Entrada.objects.filter(numero=entrada.numero).update(valor=total)
        entrada_detalle = EntradaDetalle.objects.get(id=ent.id)
        idtipodocumento = TipoDocumentoInv.objects.get(id=entrada_detalle.IdTipoDocumento_id)
        if idtipodocumento.idTipo == '03' or idtipodocumento.idTipo == '05':
            costo = 1
        else:
            costo = 0    
        if idtipodocumento.idTipo == '05':
            invinic = True
        else:
            invinic = False
        item = MaestroItem.objects.get(id=ent.IdItem_id)        
        ActualizaAcumuladosInventarios(ent.IdItem_id,ent.cantidad,ent.valor,mes,anio,'entrada',costo,invinic)
    Entrada.objects.filter(id=identrada).update(valor=total)
    
""" def MensajeNoValorEntradaInventario(request):
    identrada = request.session['id_entrada']
    mensaje1 = "Debe ingresar un valor para el item de inventario "
    mensaje2 = ""
    mensaje3 = ""
    parametro = id  
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro,'identrada':identrada}
    return render(request, 'inventarios/mensaje_no_valor_entrada_inventario.html', context)
 """
def GuardaItemEntrada(request):
    request.session['sel_item']= True
    a = request.session['sel_item']
    iditem = request.GET.get('id', None)
    cantidad = request.GET.get('cantidad', None)
    valor = request.GET.get('valor', None)
    identrada = request.session['id_entrada']
    request.session['iditem'] = iditem
    request.session['cantidad_nuevo'] = cantidad
    request.session['valor_nuevo'] = valor
    entrada = Entrada.objects.get(id=identrada)
    tipodoc = TipoDocumentoInv.objects.get(id=entrada.IdTipoDocumento_id)
    if tipodoc.idTipo == '05': 
        if valor == 'NaN':
           data={'a':1}
           return JsonResponse(data)
        else:
            AdicionaItemEntrada(iditem,cantidad,identrada,valor)
            data={'a':0}
            return JsonResponse(data)        
    else:
        AdicionaItemEntrada(iditem,cantidad,identrada,valor)
        data={'a':0}
        return JsonResponse(data)

def CreaDetalleEntradaInventarioView(request,id):
    request.session['identrada'] = id
    return redirect('selecciona_item_entrada_inventarios',id)

def GuardaIdEntrada(request):
    identrada = request.GET.get('id', None)
    request.session['id_entrada'] = identrada 
    data={'a':0}
    return JsonResponse(data)

def GuardaIdDetalleEntrada(request):
    iddetalle_entrada = request.GET.get('id', None)
    detalle_entrada = EntradaDetalle.objects.get(id=iddetalle_entrada)
    request.session['id_item_anterior'] = detalle_entrada.IdItem_id 
    request.session['id_entrada_detalle'] = iddetalle_entrada
    request.session['cantidad_anterior'] = detalle_entrada.cantidad
    request.session['numero_entrada'] = detalle_entrada.numero
    data={'a':0}
    return JsonResponse(data)

def GuardaItemEntradaNuevo(request):
    identrada = request.GET.get('id', None)
    request.session['id_entrada'] = identrada 
    iditem = request.session['iditem']
    cantidad = request.session['cantidad_nuevo']
    valor = request.session['valor_nuevo']
    AdicionaItemEntrada(iditem,cantidad,valor,identrada)
    data={'a':0}
    return JsonResponse(data)

def EntraKardexView(request):
    if request.POST:
        form1 = AnioForm(request.POST)
        return HttpResponseRedirect('kardex')
    else:
        form1 = AnioForm()
        context = {'form1':form1}
        return render(request, 'inventarios/entrada_kardex.html', context)
    
def KardexView(request):
    idanio = request.session['idanio']
    anio = Anio.objects.get(id=idanio)
    idbodega = request.session['idbodega']
    bodega = Bodega.objects.get(id=idbodega)
    items = MaestroItem.objects.filter(acumula=True,IdBodega_id=idbodega)
    #f =  ItemKardexFilter (request.GET, queryset=items)
    items = KardexTable(items)
    items.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'items':items,'anio':anio.anio,'bodega':bodega.descripcion}
    return render(request, 'inventarios/kardex.html', context) 

from django.db.models import Subquery

def KardexDetalleView(request,id):
    idanio = request.session['idanio']
    idbodega = request.session['idbodega']
    bodega = Bodega.objects.get(id=idbodega)
    anio = Anio.objects.get(id=idanio)
    anio = anio.anio
    Kardex.objects.all().delete()
    item = MaestroItem.objects.get(id=id)
    f1 = Entrada.objects.filter(anio=anio.strip())
    entradas_numero = []
    for i in f1:
          entradas_numero.append(i.numero)
    f2 = Salida.objects.filter(anio=anio.strip())
    salidas_numero = []
    for i in f2:
        salidas_numero.append(i.numero)
    q1 = EntradaDetalle.objects.filter(IdItem_id=id,numero__in=entradas_numero,IdBodega_id=idbodega)
    q2 = SalidaDetalle.objects.filter(IdItem_id=id,numero__in=salidas_numero,IdBodega_id=idbodega)
    kardex = Kardex()
    for i in q1:
        entrada = Entrada.objects.get(numero=i.numero)
        #sanio = str(entrada.fecha.year)
        #if sanio.strip() == anio.strip():
        kardex.fecha = entrada.fecha
        kardex.numero = i.numero
        kardex.IdTipoDocumento_id = i.IdTipoDocumento_id
        kardex.factura_compra = entrada.factura_compra
        kardex.orden_compra = entrada.orden_compra
        kardex.despacho = entrada.despacho
        kardex.pedido_caja = ''
        kardex.IdItem_id = i.IdItem_id
        kardex.valor = i.valor
        kardex.cantidad = i. cantidad
        kardex.valor_total = i.valor_total
        kardex.saldo = 0
        kardex.tipo_mov = 'Entrada'
        kardex.IdBodega_id = i.IdBodega_id
        kardex.save()
        kardex.id += 1       
	
    for i in q2:
        salida = Salida.objects.get(numero=i.numero)
        #sanio = str(salida.fecha.year)
        #if sanio.strip() == anio.strip():
        kardex.fecha = salida.fecha
        kardex.numero = i.numero
        kardex.IdTipoDocumento_id = i.IdTipoDocumento_id
        kardex.factura_compra = ''
        kardex.orden_compra = ''
        kardex.pedido_caja = salida.pedido_caja
        kardex.IdItem_id = i.IdItem_id
        kardex.valor = i.valor
        kardex.cantidad = i. cantidad
        kardex.valor_total = i.valor_total
        kardex.saldo = 0
        kardex.tipo_mov = 'Salida'
        kardex.IdBodega_id = i.IdBodega_id
        kardex.save()
        kardex.id += 1
    
    tsaldo = 0
    kardex = Kardex.objects.all().order_by('fecha')
    for i in kardex:
        if i.tipo_mov == 'Entrada':
            tsaldo += i.cantidad
        if i.tipo_mov == 'Salida':
            tsaldo -= i.cantidad
            #i.saldo= tsaldo  
        Kardex.objects.filter(id=i.id).update(saldo=tsaldo)
    queryset = Kardex.objects.all().order_by('fecha') 
    #f =  KardexFilter (request.GET, queryset=queryset)          
    kardex = KardexItemTable(queryset)
    kardex.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'item':item.descripcion,'kardex':kardex}
    return render(request, 'inventarios/detalle_kardex.html', context) 


class EditaInventarioFisicoView(UpdateView):
    model = InventarioFisico
    form_class = InventarioFisicoForm
    template_name = 'inventarios/inventario_fisico_form.html'
    success_url = reverse_lazy('inventario_fisico')
    
    
class FiltraItemInventarioFisicoView(SingleTableMixin, FilterView):
    table_class = ItemsInventarioFisicoTable
    model = MaestroItem
    template_name = "inventarios/inventario_fisico_items_filter.html"
    filterset_class = MaestroItemsFilter
    paginate_by = 8

def ItemInventarioFisico(request):
    request.session['sel_item']= True
    a = request.session['sel_item']
    iditem = request.GET.get('id', None)
    cantidad = request.GET.get('cantidad', None)
    idbodega = request.session['idbodega']
    #idsucursal = request.session['idsucursal']
    idanio = request.session['idanio']
    idmes = request.session['idmes']
    AdicionaItemInventarioFisico(iditem,cantidad,idanio,idmes,idbodega)
    data={'a':0}
    return JsonResponse(data)

def AdicionaItemInventarioFisico(iditem,cantidad,idanio,idmes,idbodega):
    inventario_fisico = InventarioFisico.objects.get(IdItem_id=iditem,IdBodega_id=idbodega,IdAnio_id=idanio,IdMes_id=idmes)
    InventarioFisico.objects.filter(IdItem_id=iditem,IdBodega_id=idbodega,IdAnio_id=idanio,IdMes_id=idmes).update(inv_fis = cantidad)
    inventario_fisico = InventarioFisico.objects.filter(IdBodega_id=idbodega,IdAnio_id=idanio,IdMes_id=idmes)
    for i in inventario_fisico:
        inv_acum = i.inv_acum
        inv_fis = i.inv_fis
        inventario_fisico.filter(id=i.id).update(diferencia=inv_acum-inv_fis)    

def ValidaBorraInventarioFisicoView(request):
    idanio=request.session['idanio']
    idmes=request.session['idmes']
    idbodega=request.session['idbodega']
    #idsucursal=request.session['idsucursal']
    if AjusteInventarioFisico.objects.filter(IdAnio=idanio,IdMes_id=idmes,IdBodega_id=idbodega).exists():
        #ajuste_inventario = AjusteInventarioFisico.objects.get(IdAnio=idanio,IdMes_id=idmes,IdBodega_id=idbodega)
        mensaje1 = "<El inventario físico del >"
        bodega = Bodega.objects.get(id=idbodega)
        #sucursal = Sucursal.objects.get(id=idsucursal)
        anio = Anio.objects.get(id=idanio)
        mes = Mes.objects.get(id=idmes)
        mensaje2 = "año: "+anio.anio+",mes: "+mes.descripcion+",Bodega: "+bodega.descripcion
        mensaje3 = "<Será Borrado>"
        mensaje4 = ''
        parametro = 0  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'mensaje4':mensaje4,'parametro':parametro}
        return render(request, 'inventarios/mensaje_confirma_borrado_inventario_fisico.html', context)  
    else:
       return redirect('inventario_fisico')  
    
def BorraInventarioFisicoView(request):
    idbodega = request.session['idbodega']
    #idsucursal = request.session['idsucursal']
    idanio = request.session['idanio']
    idmes = request.session['idmes']
    ajuste = AjusteInventarioFisico.objects.get(IdBodega_id=idbodega,IdAnio_id=idanio,IdMes_id=idmes)
    if ajuste.numero_ajuste_entrada !='':
        entrada = Entrada.objects.get(numero = ajuste.numero_ajuste_entrada)
        entrada_detalle = EntradaDetalle.objects.filter(numero=ajuste.numero_ajuste_entrada)
        year = entrada.fecha
        anio = year.year
        mes = year.month
        invinic = False
        for i in entrada_detalle:
            iditem = i.IdItem_id
            item = MaestroItem.objects.get(id=iditem)
            ReversaAcumuladosEntradaInventarios(iditem,i.cantidad,mes,anio,invinic)
        EntradaDetalle.objects.filter(numero=ajuste.numero_ajuste_entrada).delete()    
        Entrada.objects.filter(numero=ajuste.numero_ajuste_entrada).delete()
    if ajuste.numero_ajuste_salida !='':
        salida = Salida.objects.get(numero=ajuste.numero_ajuste_salida)
        salida_detalle = SalidaDetalle.objects.filter(numero = ajuste.numero_ajuste_salida)
        year = salida.fecha
        anio = year.year
        mes = year.month
        for i in salida_detalle:
            iditem = i.IdItem_id
            ReversaAcumuladosSalidaInventarios(iditem,i.cantidad,mes,anio)
        SalidaDetalle.objects.filter(numero=ajuste.numero_ajuste_entrada).delete()  
        Salida.objects.filter(numero = ajuste.numero_ajuste_salida).delete()

    InventarioFisico.objects.filter(IdBodega_id=idbodega,IdAnio_id=idanio,IdMes_id=idmes).delete()
    AjusteInventarioFisico.objects.filter(IdBodega_id=idbodega,IdAnio_id=idanio,IdMes_id=idmes).delete()
    mensaje1 = "Proceso Terminado : "
    mensaje2 = ""
    mensaje3 = ""
    parametro = 3 
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
    return render(request, 'inventarios/mensaje_proceso_terminado.html', context)
  

def members(request):
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())

from django.template import loader, Context

def EntraInventarioFisicoView(request):
    if request.POST:
        form1 = MesForm(request.POST)
        form2 = AnioForm(request.POST)
        return HttpResponseRedirect('inventario_fisico')
    else:
        form1 = AnioForm()
        form2 = MesForm()
        context = {'form1':form1,'form2':form2}
        return render(request, 'inventarios/entrada_inventario_fisico.html', context)
        
def AjaxBodegas(request):
    bodegas = Bodega.objects.all().values('descripcion', 'id')
    return HttpResponse( json.dumps( list(bodegas)), content_type='application/json' )

""" def AjaxSucursales(request):
    sucursales = Sucursal.objects.all().values('descripcion', 'id')
    return HttpResponse( json.dumps( list(sucursales)), content_type='application/json' ) """

def AjaxMeses(request):
    meses = Mes.objects.all().values('descripcion', 'id')
    return HttpResponse( json.dumps( list(meses)), content_type='application/json' )

def AjaxAnios(request):
    anios = Anio.objects.all().values('anio','id')
    return HttpResponse( json.dumps( list(anios)), content_type='application/json' )

def InventarioFisicoView(request):
    idanio=request.session['idanio']
    idmes=request.session['idmes']
    idbodega=request.session['idbodega']
    #idsucursal=request.session['idsucursal']
    queryset = InventarioFisico.objects.filter(IdAnio_id=idanio,IdMes_id=idmes,IdBodega_id=idbodega).order_by('IdItem') 
    f =  InventarioFisicoFilter (request.GET, queryset=queryset)          
    inventario_fisico = InventarioFisicoTable(f.qs)
    inventario_fisico.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'inventario_fisico':inventario_fisico,'filter':f}
    return render(request, 'inventarios/inventario_fisico.html', context) 

def CreaInventarioFisicoView(request):
    idbodega=request.session['idbodega']
    items = MaestroItem.objects.filter(acumula=True,IdBodega_id=idbodega)
    inventario_fisico = InventarioFisico()
    valor_defecto_bodega = ValorDefecto.objects.get(idValor='05')
    #valor_defecto_sucursal = ValorDefecto.objects.get(idValor='01')
    idanio=request.session['idanio']
    idmes=request.session['idmes']
    
    #idsucursal=request.session['idsucursal']
    sw = 0
    for item in items:
        sw = 1
        if InventarioFisico.objects.filter(IdItem=item.id,IdAnio=idanio,IdMes_id=idmes,IdBodega_id=idbodega).exists():
            #inventario_fisico = InventarioFisico.objects.get(IdItem=item.id,IdAnio=idanio,IdMes_id=idmes,IdBodega_id=idbodega)
            acumulado = AcumuladoItem.objects.get(IdItem=item.id,IdBodega_id=idbodega)  
            if acumulado.if_12>0:
                InventarioFisico.objects.filter(IdItem=item.id,IdBodega_id=idbodega,IdAnio=idanio,IdMes_id=idmes).update(inv_acum=acumulado.if_12,diferencia = acumulado.if_12-inventario_fisico.inv_fis)
        else:
            if AcumuladoItem.objects.filter(IdItem=item.id,IdBodega_id=idbodega).exists():
                acumulado = AcumuladoItem.objects.get(IdItem=item.id,IdBodega_id=idbodega)    
                inventario_fisico.IdItem_id = item.id
                inventario_fisico.inv_acum = acumulado.if_12
                inventario_fisico.IdBodega_id = idbodega
                #inventario_fisico.IdSucursal_id = idsucursal
                inventario_fisico.IdAnio_id = idanio
                inventario_fisico.IdMes_id = idmes
                inventario_fisico.save()
                inventario_fisico.id += 1
    #queryset = InventarioFisico.objects.filter(IdAnio=idanio,IdMes_id=idmes,IdBodega_id=idbodega).order_by('IdItem') 
    #f =  InventarioFisicoFilter (request.GET, queryset=queryset)          
    #inventario_fisico = InventarioFisicoTable(f.qs)
    #inventario_fisico.paginate(page=request.GET.get("page", 1), per_page=12)
    #context = {'item':item.descripcion,'inventario_fisico':inventario_fisico,'filter':f}
    mensaje1 = "Proceso Terminado : "
    mensaje2 = ""
    mensaje3 = ""
    parametro = 3 
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
    return render(request, 'inventarios/mensaje_proceso_terminado.html', context)

def ValidaAjusteInventarioFisicoView(request):
    idanio=request.session['idanio']
    idmes=request.session['idmes']
    idbodega=request.session['idbodega']
    #idsucursal=request.session['idsucursal']
    if AjusteInventarioFisico.objects.filter(IdAnio=idanio,IdMes_id=idmes,IdBodega_id=idbodega).exists():
        ajuste_inventario = AjusteInventarioFisico.objects.get(IdAnio=idanio,IdMes_id=idmes,IdBodega_id=idbodega)
        mensaje1 = "<Ajuste ya hecho para este inventario físico,>"
        mensaje2 = "<Si Desea crearlo de nuevo, debe borrar el inventario físico del: >"
        bodega = Bodega.objects.get(id=idbodega)
        #sucursal = Sucursal.objects.get(id=idsucursal)
        mensaje3 = "<año:>"+idanio+"<,mes:>"+idmes+"<,Bodega:>"+bodega.descripcion
        mensaje4 ='...........'
        parametro = 0  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'mensaje4':mensaje4,'parametro':parametro}
        return render(request, 'inventarios/mensaje_verifica_ajuste_inventario.html', context)  
    else:
       return redirect('crea_ajuste_inventario_fisico')  

class CreaAjusteInventarioFisicoView(LoginRequiredMixin,CreateView):
    model = AjusteInventarioFisico
    template_name = 'inventarios/ajuste_inventarios_form.html'
    form_class = AjusteInventariosForm

    def get_success_url(self):
        return reverse_lazy('inventario_fisico')

    def get_initial(self,*args,**kwargs):
        idbodega = self.request.session['idbodega']
        #idsucursal = self.request.session['idsucursal']
        idanio = self.request.session['idanio']
        idmes = self.request.session['idmes']
        initial=super(CreaAjusteInventarioFisicoView,self).get_initial(**kwargs)
        initial['IdAnio'] = idanio
        initial['IdMes'] = idmes
        #initial['IdSucursal'] = idsucursal
        initial['IdBodega'] = idbodega
        initial['fecha'] = date.today()
        return initial
    
    def form_valid(self, form):
        ajuste = form.save()
        ajuste.save()
        idbodega = self.request.session['idbodega']
        #idsucursal = self.request.session['idsucursal']
        idanio = self.request.session['idanio']
        idmes = self.request.session['idmes']
        inventario_fisico = InventarioFisico.objects.filter(IdAnio_id=idanio,IdMes_id=idmes,IdBodega_id=idbodega) 
        sw = 0
        tw = 0
        numero_sal = ''
        numero_ent = ''
        for item in inventario_fisico:
            if item.diferencia > 0:
                fecha = ajuste.fecha
                tipo = '07'
                year = ajuste.fecha
                anio = year.year
                mes = year.month
                num_ped=''
                detalle = 'Ajuste Inventario Físico'
                idbodega = item.IdBodega_id
                #idsucursal = item.IdSucursal_id
                idusuario = self.request.user.id
                tipodocumentoinv = TipoDocumentoInv.objects.get(idTipo=tipo)
                if sw==0:
                    anumero = tipodocumentoinv.actual +1
                    pnumero = str(anumero).zfill(tipodocumentoinv.longitud)
                    pnumero = (tipodocumentoinv.caracteres).strip()+pnumero
                    numero_sal = pnumero
                    CreaDocumentoSalidaInventariosCabeza(fecha,tipo,anio,mes,pnumero,num_ped,detalle,idusuario)
                    sw = 1
                    self.request.session['numero_salida']=pnumero
                iditem = item.IdItem_id
                cantidad = item.diferencia
                valor_venta = 0
                valor_total = 0
                pnumero=self.request.session['numero_salida']
                CreaDocumentoSalidaInventariosCuerpo(tipo,anio,mes,pnumero,num_ped,iditem,cantidad,valor_venta,valor_total)
                    
                    
            elif item.diferencia < 0: 
                fecha = ajuste.fecha
                tipo = '08'
                year = ajuste.fecha
                anio = year.year
                mes = year.month
                orden_compra=''
                despacho=''
                detalle = 'Ajuste Inventario Físico'
                idbodega = item.IdBodega_id
                #idsucursal = item.IdSucursal_id
                idusuario = self.request.user.id
                tercero = Proveedor.objects.get(identificacion='9999')
                tipodocumentoinv = TipoDocumentoInv.objects.get(idTipo=tipo)
                if tw==0:
                    anumero = tipodocumentoinv.actual+1
                    pnumero = str(anumero).zfill(tipodocumentoinv.longitud)
                    pnumero = (tipodocumentoinv.caracteres).strip()+pnumero
                    numero_ent = pnumero
                    self.request.session['numero_entrada']=pnumero
                    CreaDocumentoEntradaInventariosCabeza(fecha,tipo,anio,mes,pnumero,orden_compra,despacho,tercero.id,detalle,idusuario)
                    tw = 1
                num_ped=''
                iditem = item.IdItem_id
                cantidad = item.diferencia*-1
                valor = 0
                valor_total = 0
                invinic = False
                pnumero = self.request.session['numero_entrada']
                CreaDocumentoEntradaCuerpo(tipo,anio,mes,pnumero,iditem,cantidad,valor,valor_total,0)
                          
        for item in inventario_fisico:
            idbodega = item.IdBodega_id
            #idsucursal = item.IdSucursal_id
            iditem = item.IdItem_id
            item = MaestroItem.objects.get(id=iditem)
            acumulado = AcumuladoItem.objects.get(IdItem_id=item.id,IdBodega_id=idbodega)
            inventario_fisico = InventarioFisico.objects.get(IdItem_id=item.id,IdBodega_id=idbodega,IdAnio_id=idanio,IdMes_id=idmes)
            inv_fin = acumulado.if_12
            inv_fis =  inventario_fisico.inv_fis
            InventarioFisico.objects.filter(IdItem_id=item.id,IdBodega_id=idbodega).update(diferencia = inv_fin-inv_fis)
        ajuste = AjusteInventarioFisico()    
        ajuste.fecha = date.today()
        ajuste.IdBodega_id = idbodega
        #ajuste.IdSucursal_id = idsucursal
        ajuste.numero_ajuste_salida = self.request.session['numero_salida']
        ajuste.numero_ajuste_entrada = self.request.session['numero_entrada']
        ajuste.save() 
        #AjusteInventarioFisico.objects.filter(IdItem_id=item.id,IdBodega_id=idbodega).update(numero_ajuste_salida=numero_sal,numero_ajuste_entrada=numero_ent)
        mensaje1 = "Proceso Terminado : "
        mensaje2 = ""
        mensaje3 = ""
        parametro = 3 
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(self.request, 'inventarios/mensaje_proceso_terminado.html', context)
       
 
""" def MensajeProcesoTerminado(request,id):
    mensaje1 = "Proceso Terminado : "
    mensaje2 = ""
    mensaje3 = ""
    parametro = id  
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
    return render(request, 'inventarios/mensaje_proceso_terminado.html', context)   """

def GuardaAnio(request):
    anio = request.GET.get('anio', None)
    request.session['idanio'] = anio 
    data={'a':0}
    return JsonResponse(data)

def GuardaMes(request):
    mes = request.GET.get('mes', None)
    request.session['idmes'] = mes 
    data={'a':0}
    return JsonResponse(data)

def GuardaIdBodega(request):
    bodega = request.GET.get('bodega', None)
    request.session['idbodega'] = bodega
    data={'a':0}
    return JsonResponse(data)

def GuardaIdItemAcumulado(request):
    iditem_acumulado = request.GET.get('id', None)
    acumulado = AcumuladoItem.objects.get(id=iditem_acumulado)
    iditem = acumulado.IdItem_id
    request.session['idacumulado'] = iditem_acumulado
    request.session['iditem'] = iditem
    data={'a':0}
    return JsonResponse(data)

""" def GuardaSucursal(request):
    sucursal = request.GET.get('sucursal', None)
    request.session['idsucursal'] = sucursal 
    data={'a':0}
    return JsonResponse(data) """

def EntraCierreAnualInventarioView(request):
    if request.POST:
        form1 = AnioForm(request.POST)
        return HttpResponseRedirect('cierre_anual_inventario')
    else:
        form1 = AnioForm()
        context = {'form1':form1}
        return render(request, 'inventarios/cierre_anual_inventario.html', context)
    

def CierreAnualInventarioView(request):
    idanio=request.session['idanio']
    anio_cerrar = Anio.objects.get(id=idanio)
    cierre = CierreInventario.objects.get(anio=anio_cerrar.anio)
    if cierre.cerrado == True:
        mensaje1 = "Este año ya está cerrado"
        mensaje2=''
        mensaje3=''
        parametro = 2 
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_proceso_terminado.html', context)  
    else:
        mensaje1 = "Este proceso Traslada todos los saldo del año a cerrar,"
        mensaje2 = "al año siguiente."
        mensaje3 = "Desea hacer el cierre ?"
        parametro = 0 
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_confirma_cierre_anual_inventario.html', context)  
    #return render(request, 'inventarios/inventario_fisico.html', context) 
    
def CreaCierreAnualInventarioView(request):
    items = MaestroItem.objects.filter(acumula = True)
    idanio=request.session['idanio']
    #sucursales = Sucursal.objects.all()
    bodegas = Bodega.objects.all()
    sw = 0
    tw = 0
    tipo = '05'
    idanio = request.session['idanio']
    anio = Anio.objects.get(id=idanio)
    nanio = int(anio.anio)+1
    sanio = str(nanio) 
    #for suc in sucursales:
    for bod in bodegas:
        sw=0
        for item in items:
            if AcumuladoItem.objects.filter(IdItem=item.id,IdBodega_id=bod.id,anio=anio).exists():
                acumulado = AcumuladoItem.objects.get(IdItem=item.id,IdBodega_id=bod.id,anio=anio)
                orden_compra = ''
                despacho = ''
                detalle='Cierre de Año'
                idusuario = request.user.id
                
                tanio = sanio[-2:]
                ianio = "01/01/"+tanio
                fecha = datetime.strptime(ianio, "%d/%m/%y")
                mes = 1
                proveedor = Proveedor.objects.get(identificacion='9999')
                tercero = Tercero
                if sw == 0 and acumulado.if_12>0:
                    tipodocumentoinv = TipoDocumentoInv.objects.get(idTipo=tipo)
                    anumero = tipodocumentoinv.actual+1
                    pnumero = str(anumero).zfill(tipodocumentoinv.longitud)
                    pnumero = (tipodocumentoinv.caracteres).strip()+pnumero
                    CreaDocumentoEntradaInventariosCabeza(fecha,tipo,sanio,mes,pnumero,orden_compra,despacho,proveedor.id,detalle,idusuario)
                    sw=1
                if acumulado.if_12>0:
                    CreaDocumentoEntradaCuerpo(tipo,sanio,mes,pnumero,item.id,acumulado.if_12,acumulado.costo_prom,acumulado.costo_prom*acumulado.if_12,0)    
                    acumulado_item =  AcumuladoItem()
                    acumulado_item.IdItem_id=item.id
                    acumulado_item.IdBodega_id=bod.id
                    #acumulado_item.IdSucursal_id=suc.id    
                    acumulado_item.ii_01 = acumulado.if_12
                    acumulado_item.costo_prom = acumulado.costo_prom
                    acumulado_item.anio = sanio
                    acumulado_item.save()
                    acumulado_item.id += 1
                    tw = 1
                ActualizaAcumuladosInventarios(item.id,acumulado.if_12,acumulado.costo_prom,mes,sanio,'entrada',acumulado.costo_prom*acumulado.if_12,True)        
            
    if tw == 1:
        CierreInventario.objects.filter(anio=anio).update(cerrado=True)
        TipoDocumentoInv.objects.filter(idTipo=tipo).update(actual=anumero)        
        ValorDefecto.objects.filter(idValor='06').update(valor=nanio)
        mensaje1 = "Proceso Terminado : "
        mensaje2 = ""
        mensaje3 = ""
        parametro = 2  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_proceso_terminado.html', context)    
    else:
        mensaje1 = "Proceso Terminado, no se encontraron datos : "
        mensaje2 = ""
        mensaje3 = ""
        parametro = 2  
        context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
        return render(request, 'inventarios/mensaje_proceso_terminado.html', context)    
    
########################################################### Impresiones ###############################################
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

def ImpresionMedidasXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
        
    worksheet.write('A1','Id' )
    worksheet.write('B1','Descripción' )
    medidas = Medida.objects.all()
    n=2
    for j in medidas:     
        nn = str(n)
        id = j.idMedida
        descripcion = j.descripcion
        exec("worksheet.write('A"+nn+"','"+id+"' )")
        exec("worksheet.write('B"+nn+"','"+descripcion+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'medidas_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response   

def ImpresionSubGruposInventarioXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
        
    worksheet.write('A1','Id' )
    worksheet.write('B1','Descripción' )
    if request.session['lista_id_filtro_subgrupos'] == False:
        grupos = Grupo.objects.all()
    else:
        grupos = Grupo.objects.filter(id__in=request.session['lista_id_subgrupos'])   
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

def ImpresionSubGruposInventarioXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    if request.session['lista_id_filtro_subgrupos'] == False:
        grupos = Grupo.objects.all().order_by('idGrupo')
    else:
        grupos = Grupo.objects.filter(id__in=request.session['lista_id_subgrupos']) 
    n=2
    for j in grupos:
        subgrupos = SubGrupo.objects.filter(IdGrupo_id=j.id)     
        nn = str(n)
        id = j.idGrupo
        descripcion = j.descripcion
        worksheet.write('A1','Id' )
        worksheet.write('B1','Descripción' )
        #exec("worksheet.write('A"+nn+"','ID')")
        #exec("worksheet.write('B"+nn+"','Descripcion')")
        exec("worksheet.write('A"+nn+"','"+id+"' )")
        exec("worksheet.write('B"+nn+"','"+descripcion+"' )")    
        n += 1
        #worksheet.write('A1','Id' )
        #worksheet.write('B1','Descripción' )
        for k in subgrupos:
            nn = str(n)
            id = k.idSubGrupo
            descripcion = k.descripcion
            exec("worksheet.write('C"+nn+"','"+id+"' )")
            exec("worksheet.write('D"+nn+"','"+descripcion+"' )")    
            n += 1
    workbook.close()
    output.seek(0)
    filename = 'sub_grupos_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response    

def ImpresionGruposInventarioView(request):
    grupos = Grupo.objects.all().order_by('id')
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
    pdf.drawString(200, y, u"GRUPOS INVENTARIO")
    pdf.setFont("Helvetica", 9)
    y -= 90
    encabezados = ('Código','Descripción')
    detalle = [(grupo.id,grupo.descripcion) for grupo in grupos]
    detalle_grupo = Table([encabezados] + detalle, colWidths=[1.5 * cm, 10 * cm])
    detalle_grupo.setStyle(TableStyle(
    [
        #La primera fila(encabezados) va a estar centrada
        ('ALIGN',(0,0),(3,0),'CENTER'),
        #Los bordes de todas las celdas serán de color negro y con un grosor de 1
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        #El tamaño de las letras de cada una de las celdas será de 10
        ('FONTSIZE', (0, 0), (-1, -1),7),
    ]
    ))
    #total_pagos = total_pagos.aggregate(Sum('valor'))['valor__sum']
    b= 0
    for j in detalle:
        b += 1
    y = y - b*18
    if y<= 35:
        pdf.showPage()
        y= 700
    detalle_grupo.wrapOn(pdf, 300, 800)
    detalle_grupo.drawOn(pdf, 40,y)
    y -= 10
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionMedidasView(request):
    medidas = Medida.objects.all().order_by('id')
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
    pdf.drawString(200, y, u"MEDIDAS INVENTARIO")
    pdf.setFont("Helvetica", 9)
    y -= 90
    encabezados = ('Código','Descripción')
    detalle = [(medida.id,medida.descripcion) for medida in medidas]
    detalle_grupo = Table([encabezados] + detalle, colWidths=[1.5 * cm, 10 * cm])
    detalle_grupo.setStyle(TableStyle(
    [
        #La primera fila(encabezados) va a estar centrada
        ('ALIGN',(0,0),(3,0),'CENTER'),
        #Los bordes de todas las celdas serán de color negro y con un grosor de 1
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        #El tamaño de las letras de cada una de las celdas será de 10
        ('FONTSIZE', (0, 0), (-1, -1),7),
    ]
    ))
    #total_pagos = total_pagos.aggregate(Sum('valor'))['valor__sum']
    b= 0
    for j in detalle:
        b += 1
    y = y - b*18
    if y<= 35:
        pdf.showPage()
        y= 700
    detalle_grupo.wrapOn(pdf, 300, 800)
    detalle_grupo.drawOn(pdf, 40,y)
    y -= 10
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionBodegasView(request):
    bodegas = Bodega.objects.all().order_by('id')
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
    pdf.drawString(200, y, u"BODEGAS INVENTARIO")
    pdf.setFont("Helvetica", 9)
    y -= 90
    registros = Bodega.objects.all().count()
    encabezados = ('Código','Descripción','Dirección','Teléfono','Email')
    detalle = [(bodega.idBodega,bodega.descripcion,bodega.direccion[0:30],bodega.telefonos,bodega.email_bodega) for bodega in bodegas]
    detalle_grupo = Table([encabezados] + detalle, colWidths=[1.5 * cm, 4 * cm, 4.5 * cm, 3.5 * cm,3.5 * cm])
    detalle_grupo.setStyle(TableStyle(
    [
        #La primera fila(encabezados) va a estar centrada
        ('ALIGN',(0,0),(3,0),'CENTER'),
        #Los bordes de todas las celdas serán de color negro y con un grosor de 1
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        #El tamaño de las letras de cada una de las celdas será de 10
        ('FONTSIZE', (0, 0), (-1, -1),7),
    ]
    ))
    #total_pagos = total_pagos.aggregate(Sum('valor'))['valor__sum']
    y = y - registros*16
    if y<= 35:
        pdf.showPage()
        y= 700
    detalle_grupo.wrapOn(pdf, 300, 800)
    detalle_grupo.drawOn(pdf, 40,y)
    y -= 10
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionBodegasXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
        
    worksheet.write('A1','Id' )
    worksheet.write('B1','Descripción' )
    worksheet.write('C1','Direccion' )
    worksheet.write('D1','Tel´fono' )
    worksheet.write('E1','Responsable' )
    worksheet.write('F1','Email' )
    bodegas = Bodega.objects.all()
    n=2
    for j in bodegas:     
        nn = str(n)
        descripcion = j.descripcion
        exec("worksheet.write('A"+nn+"','"+str(j.id)+"' )")
        exec("worksheet.write('B"+nn+"','"+j.descripcion+"' )")
        exec("worksheet.write('C"+nn+"','"+j.direccion+"' )")
        exec("worksheet.write('D"+nn+"','"+j.telefonos+"' )")
        exec("worksheet.write('E"+nn+"','"+j.responsable+"' )")
        exec("worksheet.write('F"+nn+"','"+j.email_bodega+"' )")   
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'bodegas_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response   

def ImpresionSubGruposInventarioView(request):
    grupos = Grupo.objects.all().order_by('id')
    subgrupos = SubGrupo.objects.all().order_by('IdGrupo')
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
    pdf.drawString(200, y, u"SUBGRUPOS INVENTARIO")
    pdf.setFont("Helvetica", 9)
    y -= 90
    encabezados = ('Código','Descripción')
    for grupo in grupos:
        y -= 10
        pdf.drawString(120, y, u"GRUPO: "+grupo.descripcion)
        y -= 30
        subgrupos = SubGrupo.objects.filter(IdGrupo_id=grupo.id)
        detalle = [(subgrupo.idSubGrupo,subgrupo.descripcion) for subgrupo in subgrupos]
        detalle_subgrupo = Table([encabezados] + detalle, colWidths=[1.5 * cm,5 * cm])
        detalle_subgrupo.setStyle(TableStyle(
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
        for j in detalle:
            b += 1
        y = y - b*18
        if y<= 35:
            pdf.showPage()
            y= 700
        detalle_subgrupo.wrapOn(pdf, 300, 800)
        detalle_subgrupo.drawOn(pdf, 120,y)
        y -= 10
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionItemsInventarioGrupoSubgruposView(request):
    grupos = Grupo.objects.all().order_by('id')
    subgrupos = SubGrupo.objects.all().order_by('IdGrupo')
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
    pdf.drawString(200, y, u"ITEMS INVENTARIO")
    pdf.setFont("Helvetica", 9)
    y -= 40
    for grupo in grupos:
        items = MaestroItem.objects.filter(IdGrupo_id=grupo.id)
        if items: 
            pdf.setFont("Helvetica", 8)
            y -= 10
            pdf.drawString(10, y, u"GRUPO: "+grupo.descripcion)
            y -= 10
            subgrupos = SubGrupo.objects.filter(IdGrupo_id=grupo.id)
            for subgrupo in subgrupos:
                items = MaestroItem.objects.filter(IdGrupo_id=grupo.id,IdSubGrupo_id=subgrupo.id,id__in=request.session['lista_id_filtro_items'])
                if items:
                    y -= 10
                    pdf.drawString(20, y, u""+subgrupo.descripcion)
                    y -= 10
                    encabezados =('descripcion','U.Medida','Marca','Val.Venta','Val.Compra','Tipo Prod.','% Iva')
                    items = MaestroItem.objects.filter(IdGrupo_id=grupo.id,IdSubGrupo_id=subgrupo.id)
                    if items:  
                        detalle = [(item.descripcion[0:60],item.IdUnidadMedida.descripcion[0:30],item.marca[0:30],'{:,}'.format(item.valor_venta),'{:,}'.format(item.valor_compra),item.tipo_producto,'{:,}'.format(item.por_iva)) for item in items]
                        detalle_item = Table([encabezados] + detalle, colWidths=[6 * cm,3 * cm,3 * cm,2 * cm,1.5 * cm,1.5 * cm])
                        detalle_item.setStyle(TableStyle(
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
                        y = y - b*28
                        if y<= 35:
                            pdf.showPage()
                            y= 750
                        pdf.setFont("Helvetica", 7)    
                        detalle_item.wrapOn(pdf, 300, 800)
                        detalle_item.drawOn(pdf, 20,y)
                        y -= 10
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionItemsInventarioGrupoSubgruposXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    grupos = Grupo.objects.all().order_by('descripcion')
    n=2
    nn = str(n)
    exec("worksheet.write('A"+nn+"','Descripción' )")
    exec("worksheet.write('B"+nn+"','Un.Medida' )")
    exec("worksheet.write('C"+nn+"','Marca' )")
    exec("worksheet.write('D"+nn+"','Val.Venta' )")    
    exec("worksheet.write('E"+nn+"','Val.Compra' )")
    exec("worksheet.write('F"+nn+"','Tipo Prod.' )")
    n += 1
    for j in grupos:
        nn = str(n)
        subgrupos = SubGrupo.objects.filter(IdGrupo_id=j.id)     
        exec("worksheet.write('A"+nn+"','GRUPO: "+j.descripcion+"' )")
        n += 1
        for k in subgrupos:
            nn = str(n)
            exec("worksheet.write('A"+nn+"','SUBGRUPO: "+k.descripcion+"' )")    
            n += 1
            items = MaestroItem.objects.filter(IdGrupo_id=j.id,IdSubGrupo_id=k.id,id__in=request.session['lista_id_filtro_items'])
            for item in items:
                nn = str(n)
                exec("worksheet.write('A"+nn+"','"+item.descripcion+"')")
                exec("worksheet.write('B"+nn+"','"+item.IdUnidadMedida.descripcion+"')")
                exec("worksheet.write('C"+nn+"','"+item.marca+"' )")
                exec("worksheet.write('D"+nn+"','"+str(item.valor_venta)+"')")    
                exec("worksheet.write('E"+nn+"','"+str(item.valor_compra)+"')")
                exec("worksheet.write('F"+nn+"','"+item.tipo_producto+"' )")    
                n += 1
        n += 1        
    workbook.close()
    output.seek(0)
    filename = 'grupos_sub_grupos_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response    

""" def ReporteItemsGrupoSubgrupo(request):
    grupos = Grupo.objects.all().order_by('descripcion')
    data = []
    for grupo in grupos:
        subgrupos = SubGrupo.objects.filter(IdGrupo=grupo).order_by('descripcion')
        subgrupos_data = []
        for subgrupo in subgrupos:
            items = MaestroItem.objects.filter(IdGrupo=grupo, IdSubGrupo=subgrupo).order_by('descripcion')
            subgrupos_data.append({
                'subgrupo': subgrupo,
                'items': items
            })
        data.append({
            'grupo': grupo,
            'subgrupos': subgrupos_data
        })
    return render(request, 'inventarios/items_inventario_grupos_subgrupos.html', {'data': data})

def ReporteItemsPrecios(request):
    grupos = Grupo.objects.all().order_by('descripcion')
    data = []
    for grupo in grupos:
        subgrupos = SubGrupo.objects.filter(IdGrupo=grupo).order_by('descripcion')
        subgrupos_data = []
        for subgrupo in subgrupos:
            items = MaestroItem.objects.filter(IdGrupo=grupo, IdSubGrupo=subgrupo).order_by('descripcion')
            subgrupos_data.append({
                'subgrupo': subgrupo,
                'items': items
            })
        data.append({
            'grupo': grupo,
            'subgrupos': subgrupos_data
        })
    return render(request, 'inventarios/items_inventario_grupos_subgrupos.html', {'data': data})

def ReporteItemsAlfabetico(request):
    grupos = Grupo.objects.all().order_by('descripcion')
    data = []
    for grupo in grupos:
        subgrupos = SubGrupo.objects.filter(IdGrupo=grupo).order_by('descripcion')
        subgrupos_data = []
        for subgrupo in subgrupos:
            items = MaestroItem.objects.filter(IdGrupo=grupo, IdSubGrupo=subgrupo).order_by('descripcion')
            subgrupos_data.append({
                'subgrupo': subgrupo,
                'items': items
            })
        data.append({
            'grupo': grupo,
            'subgrupos': subgrupos_data
        })
    return render(request, 'inventarios/items_inventario_grupos_subgrupos.html', {'data': data}) """

def ImpresionItemsAlfabeticoView(request):
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
    pdf.drawString(200, y, u"ITEMS INVENTARIO")
    pdf.setFont("Helvetica", 9)
    y -= 40
    encabezados =('descripcion','U.Medida','Marca','Val.Venta','Val.Compra','Tipo Prod.','% Iva')
    items = MaestroItem.objects.filter(id__in=request.session['lista_id_filtro_items']).order_by('descripcion')
    registros = MaestroItem.objects.filter(id__in=request.session['lista_id_filtro_items']).count()
    detalle = [(item.descripcion[0:40],item.IdUnidadMedida.descripcion[0:30],item.marca[0:25],'{:,}'.format(item.valor_venta),'{:,}'.format(item.valor_compra),item.tipo_producto,'{:,}'.format(item.por_iva)) for item in items]
    detalle_item = Table([encabezados] + detalle, colWidths=[6 * cm,3 * cm,2 * cm,2 * cm,2 * cm,1.5 * cm])
    detalle_item.setStyle(TableStyle(
    [
    #La primera fila(encabezados) va a estar centrada
    ('ALIGN',(0,0),(3,0),'CENTER'),
    #Los bordes de todas las celdas serán de color negro y con un grosor de 1
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    #El tamaño de las letras de cada una de las celdas será de 10
    ('FONTSIZE', (0, 0), (-1, -1),7),
    ]
    ))
    y = y - registros*(18)
    if y<= 35:
        pdf.showPage()
        y= 750
    pdf.setFont("Helvetica", 7)    
    detalle_item.wrapOn(pdf, 300, 800)
    detalle_item.drawOn(pdf, 20,y)
    y -= 10
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionItemsAlfabeticoXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    grupos = Grupo.objects.all().order_by('-descripcion')
    n=2
    items = MaestroItem.objects.filter(id__in=request.session['lista_id_filtro_items']).order_by('descripcion')
    nn = str(n)
    exec("worksheet.write('C"+nn+"','Descripción' )")
    exec("worksheet.write('D"+nn+"','Un.Medida' )")
    exec("worksheet.write('E"+nn+"','Marca' )")
    exec("worksheet.write('F"+nn+"','Val.Venta' )")    
    exec("worksheet.write('G"+nn+"','Val.Compra' )")
    exec("worksheet.write('H"+nn+"','Tipo Prod.' )")
    n += 1
    for item in items:
        nn = str(n)
        exec("worksheet.write('C"+nn+"','"+item.descripcion+"' )")
        exec("worksheet.write('D"+nn+"','"+item.IdUnidadMedida.descripcion+"' )")
        exec("worksheet.write('E"+nn+"','"+item.marca+"' )")
        exec("worksheet.write('F"+nn+"','"+str(item.valor_venta)+"' )")
        exec("worksheet.write('G"+nn+"','"+str(item.valor_compra)+"' )")
        exec("worksheet.write('H"+nn+"','"+item.tipo_producto+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'items_inventario_alfabetico.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response  

def ImpresionItemsPreciosView(request):
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
    pdf.drawString(200, y, u"ITEMS INVENTARIO PRECIOS")
    pdf.setFont("Helvetica", 9)
    y -= 40
    encabezados =('descripcion','Unidad Medida','Val.Venta','Val.Compra','Utilidad')
    items = MaestroItem.objects.filter(id__in=request.session['lista_id_filtro_items']).annotate(utilidad=ExpressionWrapper(F('valor_venta') - F('valor_compra'),output_field=DecimalField(max_digits=10, decimal_places=2)))
    registros = MaestroItem.objects.filter(id__in=request.session['lista_id_filtro_items']).count()
    detalle = [(item.descripcion[0:40],item.IdUnidadMedida.descripcion[0:30],'{:,}'.format(item.valor_venta),'{:,}'.format(item.valor_compra),'{:,}'.format(item.utilidad)) for item in items]
    detalle_item = Table([encabezados] + detalle, colWidths=[6 * cm,3 * cm,2 * cm,2 * cm,2 * cm])
    detalle_item.setStyle(TableStyle(
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
    y = y - registros*18
    if y<= 35:
        pdf.showPage()
        y= 750
    pdf.setFont("Helvetica", 7)    
    detalle_item.wrapOn(pdf, 300, 800)
    detalle_item.drawOn(pdf, 20,y)
    y -= 10
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionItemsPreciosXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    grupos = Grupo.objects.all().order_by('descripcion')
    n=2
    items = MaestroItem.objects.filter(id__in=request.session['lista_id_filtro_items']).order_by('descripcion')
    nn = str(n)
    exec("worksheet.write('A"+nn+"','Descripción' )")
    exec("worksheet.write('B"+nn+"','Un.Medida' )")
    exec("worksheet.write('C"+nn+"','Marca' )")
    exec("worksheet.write('D"+nn+"','Val.Venta' )")    
    exec("worksheet.write('E"+nn+"','Val.Compra' )")
    exec("worksheet.write('F"+nn+"','Utilidad' )")
    n += 1
    for item in items:
        nn = str(n)
        utilidad = item.valor_venta - item.valor_compra
        exec("worksheet.write('A"+nn+"','"+item.descripcion+"' )")
        exec("worksheet.write('B"+nn+"','"+item.IdUnidadMedida.descripcion+"' )")
        exec("worksheet.write('C"+nn+"','"+item.marca+"' )")
        exec("worksheet.write('D"+nn+"','"+str(item.valor_venta)+"' )")
        exec("worksheet.write('E"+nn+"','"+str(item.valor_compra)+"' )")
        exec("worksheet.write('F"+nn+"','"+str(utilidad)+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'items_inventario_precios.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response  

def ImpresionItemsPuntoCompraView(request):
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
    pdf.drawString(200, y, u"ITEMS EN PUNTO DE COMPRA")
    pdf.setFont("Helvetica", 9)
    y -= 20
    # Trae el campo if_12 de AcumuladoItem para cada MaestroItem según la bodega (por ejemplo, idbodega)
    val_def = ValorDefecto.objects.get(idValor='06')
    anio = val_def.valor    
    bodegas = Bodega.objects.all()
    sw=0
    for bodega in bodegas:
        #items = MaestroItem.objects.filter(IdBodega_id=bodega.id).annotate(if_12=F('acumuladoitem__if_12')).annotate(cant_compra=ExpressionWrapper(F('cant_minima') - F('if_12'),output_field=IntegerField()))
        #acum_qs = AcumuladoItem.objects.filter(IdItem=OuterRef('pk'),IdBodega=OuterRef('IdBodega'),anio=anio).values('if_12')[:1] 
        #items = MaestroItem.objects.annotate(if_12=Subquery(acum_qs)).annotate(cant_compra=ExpressionWrapper(F('cant_minima') - F('if_12'),output_field=IntegerField())).values_list('id','descripcion','IdUnidadMedida','if_12', 'cant_minima', 'cant_compra')
        lista_ids = request.session['lista_id_filtro_items']
        acum_qs = AcumuladoItem.objects.filter(IdItem=OuterRef('pk'),IdBodega=OuterRef('IdBodega'),anio=anio).values('if_12')[:1]
        titems = MaestroItem.objects.filter(id__in=lista_ids,IdBodega_id=bodega.id).annotate(if_12=Subquery(acum_qs)).annotate(cant_compra=ExpressionWrapper(F('cant_minima') - F('if_12'),output_field=IntegerField())).values_list('id', 'descripcion', 'IdUnidadMedida__descripcion', 'if_12', 'cant_minima', 'cant_compra')
        items = []
        for i in titems:
            if i[5]:
                if i[5]> 0:  # Solo incluir si la cantidad a comprar es mayor que 0
                    items.append((i[0], i[1], i[2], i[3], i[4], i[5]))
        if items:
            registros = MaestroItem.objects.filter(id__in=lista_ids,IdBodega_id=bodega.id).count()
            if sw == 0:
                encabezados =('descripcion','Unidad Medida','Stock','Cant. Mimima','Cant. Comprar')  
                detalle = [(item[1],item[2],item[3],item[4],item[5]) for item in items if item[5]>0]
                detalle_item = Table([encabezados] + detalle, colWidths=[6 * cm,3 * cm,3 * cm,3 * cm,3 * cm])
                detalle_item.setStyle(TableStyle(
                [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1),7),
                ]
                ))
                y = y - registros*11
                if y<= 35:
                    pdf.showPage()
                    y= 750
            else:
                encabezados =''  
                detalle = [(item[1],item[2],item[3],item[4],item[5]) for item in items]
                detalle_item = Table(detalle, colWidths=[6 * cm,3 * cm,3 * cm,3 * cm,3 * cm])    
                detalle_item.setStyle(TableStyle(
                [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'LEFT'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1),7),
                ]
                ))
                y = y - registros*4
                if y<= 35:
                    pdf.showPage()
                    y= 750
            sw=1
            
            pdf.setFont("Helvetica", 7)    
            detalle_item.wrapOn(pdf, 300, 800)
            detalle_item.drawOn(pdf, 20,y)
            y -= 10
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionItemsPuntoCompraXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    grupos = Grupo.objects.all().order_by('descripcion')
    n=2
    items = MaestroItem.objects.filter(id__in=request.session['lista_id_filtro_items']).order_by('descripcion')
    nn = str(n)
    exec("worksheet.write('A"+nn+"','Descripción' )")
    exec("worksheet.write('B"+nn+"','Un.Medida' )")
    exec("worksheet.write('C"+nn+"','Marca' )")
    exec("worksheet.write('D"+nn+"','Val.Venta' )")    
    exec("worksheet.write('E"+nn+"','Val.Compra' )")
    exec("worksheet.write('F"+nn+"','Cantidad Comprar' )")
    n += 1
    for item in items:
        nn = str(n)
        maestroItem = MaestroItem.objects.get(id=item.id)
        idbodega = maestroItem.IdBodega_id
        if AcumuladoItem.objects.filter(IdItem_id=item.id, IdBodega_id=idbodega).exists():
            acum = AcumuladoItem.objects.get(IdItem_id=item.id, IdBodega_id=idbodega)
            valor_def=ValorDefecto.objects.get(idValor='06')
            anio = valor_def.valor  
            cantidad_compra = item.cant_minima - acum.if_12
            if cantidad_compra>0:
                exec("worksheet.write('A"+nn+"','"+item.descripcion+"' )")
                exec("worksheet.write('B"+nn+"','"+item.IdUnidadMedida.descripcion+"' )")
                exec("worksheet.write('C"+nn+"','"+item.marca+"' )")
                exec("worksheet.write('D"+nn+"','"+str(item.valor_venta)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(item.valor_compra)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(cantidad_compra)+"' )")
                n += 1
    workbook.close()
    output.seek(0)
    filename = 'items_inventario_punto_compra.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response  

def ImpresionItemsInventarioXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    grupos = Grupo.objects.all().order_by('idGrupo')
    n=2
    for j in grupos:
        subgrupos = SubGrupo.objects.filter(IdGrupo_id=j.id)     
        nn = str(n)
        id = j.idGrupo
        descripcion = j.descripcion
        worksheet.write('A1','Id' )
        worksheet.write('B1','Descripción' )
        exec("worksheet.write('A"+nn+"','"+id+"' )")
        exec("worksheet.write('B"+nn+"','"+descripcion+"' )")    
        n += 1
        for k in subgrupos:
            nn = str(n)
            id = k.idSubGrupo
            descripcion = k.descripcion
            exec("worksheet.write('B"+nn+"','"+id+"' )")
            exec("worksheet.write('C"+nn+"','"+descripcion+"' )")    
            n += 1
            items = MaestroItem.objects.filter(IdGrupo_id=j.id,IdSubGrupo_id=k.id)
            nn = str(n)
            exec("worksheet.write('C"+nn+"','Código' )")
            exec("worksheet.write('D"+nn+"','Descripción' )")
            exec("worksheet.write('E"+nn+"','Un.Medida' )")
            exec("worksheet.write('F"+nn+"','Marca' )")
            exec("worksheet.write('G"+nn+"','Val.Venta' )")    
            exec("worksheet.write('H"+nn+"','Val.Compra' )")
            exec("worksheet.write('I"+nn+"','Tipo Prod.' )")
            n += 1
            for item in items:
                nn = str(n)
                exec("worksheet.write('C"+nn+"','"+item.idItem+"' )")
                exec("worksheet.write('D"+nn+"','"+item.descripcion+"' )")
                exec("worksheet.write('E"+nn+"','"+item.IdUnidadMedida.descripcion+"' )")
                exec("worksheet.write('F"+nn+"','"+item.marca+"' )")
                exec("worksheet.write('G"+nn+"','"+str(item.valor_venta)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(item.valor_compra)+"' )")
                exec("worksheet.write('I"+nn+"','"+item.tipo_producto+"' )")
                n += 1
    workbook.close()
    output.seek(0)
    filename = 'items_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response  
    

def ImpresionAcumuladosInventarioView(request):
    grupos = Grupo.objects.all().order_by('id')
    #subgrupos = SubGrupo.objects.all().order_by('IdGrupo')
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
    pdf.drawString(200, y, u"ACUMULADO ITEMS INVENTARIO")
    pdf.setFont("Helvetica", 9)
    y -= 40
    bodegas = Bodega.objects.all()
    total_bodega = 0
    #for bodega in bodegas:
    idbodega = request.session['idbodega']
    bodega = Bodega.objects.get(id=idbodega)
    items = MaestroItem.objects.filter(acumula=True)
    acum = AcumuladoItem.objects.filter(IdBodega_id=bodega.id)
    if bodega.idBodega != '*':
        y -= 20
        pdf.drawString(20, y, u"BODEGA : "+bodega.descripcion)
        y -= 20
    for item in items:
        if request.session['items_acumulado_filtro']:
            lista_filtro = request.session['items_acumulado_filtro']
            acumulados = AcumuladoItem.objects.filter(IdBodega_id=idbodega,IdItem_id=item.id,id__in=lista_filtro)
        else:    
            acumulados = AcumuladoItem.objects.filter(IdBodega_id=idbodega,IdItem_id=item.id)
        for acum in acumulados:
            total_bodega = total_bodega + acum.if_12*acum.costo_prom
            encabezados =('Descripción','Costo Prom.','Cant. Máxima','Cant. Mínima')
            detalle = [(P(acum.IdItem.descripcion),'{:,}'.format(acum.costo_prom),'{:,}'.format(acum.cant_maxima),'{:,}'.format(acum.cant_minima)) for acum in acumulados]
            detalle_item = Table([encabezados] + detalle, colWidths=[8 * cm,1.8 * cm,1.8 * cm,1.8 * cm])
            detalle_item.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1),7),
            ]
            ))
            y = y - 25
            if y<= 35:
                pdf.showPage()
                y= 750
            pdf.setFont("Helvetica", 7)    
            detalle_item.wrapOn(pdf, 300, 800)
            detalle_item.drawOn(pdf, 20,y)
            
            encabezados =('Mes','Inv.Inic','Valor','Entradas','Valor','Salidas','Valor','Inv.Final','Valor')
            detalle = [('Enero','{:,}'.format(acum.ii_01),'{:,}'.format(acum.ii_01*acum.costo_prom),'{:,}'.format(acum.ent_01),'{:,}'.format(acum.ent_01*acum.costo_prom),'{:,}'.format(acum.sal_01),'{:,}'.format(acum.sal_01*acum.costo_prom),'{:,}'.format(acum.if_01),'{:,}'.format(acum.if_01*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Febrero','{:,}'.format(acum.ii_02),'{:,}'.format(acum.ii_02*acum.costo_prom),'{:,}'.format(acum.ent_02),'{:,}'.format(acum.ent_02*acum.costo_prom),'{:,}'.format(acum.sal_02),'{:,}'.format(acum.sal_02*acum.costo_prom),'{:,}'.format(acum.if_02),'{:,}'.format(acum.if_02*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Marzo','{:,}'.format(acum.ii_03),'{:,}'.format(acum.ii_02*acum.costo_prom),'{:,}'.format(acum.ent_03),'{:,}'.format(acum.ent_03*acum.costo_prom),'{:,}'.format(acum.sal_03),'{:,}'.format(acum.sal_03*acum.costo_prom),'{:,}'.format(acum.if_03),'{:,}'.format(acum.if_03*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Abril','{:,}'.format(acum.ii_04),'{:,}'.format(acum.ii_04*acum.costo_prom),'{:,}'.format(acum.ent_04),'{:,}'.format(acum.ent_04*acum.costo_prom),'{:,}'.format(acum.sal_04),'{:,}'.format(acum.sal_04*acum.costo_prom),'{:,}'.format(acum.if_04),'{:,}'.format(acum.if_04*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Mayo','{:,}'.format(acum.ii_05),'{:,}'.format(acum.ii_05*acum.costo_prom),'{:,}'.format(acum.ent_05),'{:,}'.format(acum.ent_05*acum.costo_prom),'{:,}'.format(acum.sal_05),'{:,}'.format(acum.sal_05*acum.costo_prom),'{:,}'.format(acum.if_05),'{:,}'.format(acum.if_05*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Junio','{:,}'.format(acum.ii_06),'{:,}'.format(acum.ii_06*acum.costo_prom),'{:,}'.format(acum.ent_06),'{:,}'.format(acum.ent_06*acum.costo_prom),'{:,}'.format(acum.sal_06),'{:,}'.format(acum.sal_06*acum.costo_prom),'{:,}'.format(acum.if_06),'{:,}'.format(acum.if_06*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Julio','{:,}'.format(acum.ii_07),'{:,}'.format(acum.ii_07*acum.costo_prom),'{:,}'.format(acum.ent_07),'{:,}'.format(acum.ent_07*acum.costo_prom),'{:,}'.format(acum.sal_07),'{:,}'.format(acum.sal_07*acum.costo_prom),'{:,}'.format(acum.if_07),'{:,}'.format(acum.if_03*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Agosto','{:,}'.format(acum.ii_08),'{:,}'.format(acum.ii_08*acum.costo_prom),'{:,}'.format(acum.ent_08),'{:,}'.format(acum.ent_08*acum.costo_prom),'{:,}'.format(acum.sal_08),'{:,}'.format(acum.sal_08*acum.costo_prom),'{:,}'.format(acum.if_08),'{:,}'.format(acum.if_08*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Septiembre','{:,}'.format(acum.ii_09),'{:,}'.format(acum.ii_09*acum.costo_prom),'{:,}'.format(acum.ent_09),'{:,}'.format(acum.ent_09*acum.costo_prom),'{:,}'.format(acum.sal_09),'{:,}'.format(acum.sal_09*acum.costo_prom),'{:,}'.format(acum.if_09),'{:,}'.format(acum.if_09*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Octubre','{:,}'.format(acum.ii_10),'{:,}'.format(acum.ii_10*acum.costo_prom),'{:,}'.format(acum.ent_10),'{:,}'.format(acum.ent_10*acum.costo_prom),'{:,}'.format(acum.sal_10),'{:,}'.format(acum.sal_10*acum.costo_prom),'{:,}'.format(acum.if_10),'{:,}'.format(acum.if_10*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Noviembre','{:,}'.format(acum.ii_11),'{:,}'.format(acum.ii_11*acum.costo_prom),'{:,}'.format(acum.ent_11),'{:,}'.format(acum.ent_11*acum.costo_prom),'{:,}'.format(acum.sal_11),'{:,}'.format(acum.sal_11*acum.costo_prom),'{:,}'.format(acum.if_11),'{:,}'.format(acum.if_11*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Diciembre','{:,}'.format(acum.ii_12),'{:,}'.format(acum.ii_12*acum.costo_prom),'{:,}'.format(acum.ent_12),'{:,}'.format(acum.ent_12*acum.costo_prom),'{:,}'.format(acum.sal_12),'{:,}'.format(acum.sal_12*acum.costo_prom),'{:,}'.format(acum.if_12),'{:,}'.format(acum.if_12*acum.costo_prom)) for acum in acumulados]
            detalle_item = Table([encabezados] + detalle, colWidths=[2 * cm,2 * cm,2 * cm,2 * cm,2 * cm,2 * cm,2 * cm,2 * cm,2 * cm])
            detalle_item.setStyle(TableStyle(
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
            y = y - b*20
            if y<= 10:
                pdf.showPage()
                y= 600
            pdf.setFont("Helvetica", 7)    
            detalle_item.wrapOn(pdf, 300, 800)
            detalle_item.drawOn(pdf, 20,y)
            y -=20                         
    pdf.setFont("Helvetica", 9)
    pdf.drawString(240, y, u"Total Bodega      : "+('{:,}'.format(total_bodega)))    
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionAcumuladosInventarioUnItemView(request,iditem):
    grupos = Grupo.objects.all().order_by('id')
    #subgrupos = SubGrupo.objects.all().order_by('IdGrupo')
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
    pdf.drawString(200, y, u"ACUMULADO ITEMS INVENTARIO")
    pdf.setFont("Helvetica", 9)
    y -= 40
    idbodega = request.session['idbodega']
    bodega = Bodega.objects.get(id=idbodega)
    total_bodega = 0
    items = MaestroItem.objects.filter(acumula=True,id=iditem)
    acum = AcumuladoItem.objects.filter(IdBodega_id=bodega.id)
    if bodega.idBodega != '*':
        y -= 20
        pdf.drawString(20, y, u"BODEGA : "+bodega.descripcion)
        y -= 20
    for item in items:
        if request.session['items_acumulado_filtro']:
            lista_filtro = request.session['items_acumulado_filtro']
            acumulados = AcumuladoItem.objects.filter(IdBodega_id=bodega.id,IdItem_id=item.id,id__in=lista_filtro)
        else:    
            acumulados = AcumuladoItem.objects.filter(IdBodega_id=bodega.id,IdItem_id=item.id)
        for acum in acumulados:
            total_bodega = total_bodega + acum.if_12*acum.costo_prom
            encabezados =('Descripción','Costo Prom.','Cant. Máxima','Cant. Mínima')
            detalle = [(P(acum.IdItem.descripcion),'{:,}'.format(acum.costo_prom),'{:,}'.format(acum.cant_maxima),'{:,}'.format(acum.cant_minima)) for acum in acumulados]
            detalle_item = Table([encabezados] + detalle, colWidths=[8 * cm,1.8 * cm,1.8 * cm,1.8 * cm])
            detalle_item.setStyle(TableStyle(
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
            y = y - b*25
            if y<= 35:
                pdf.showPage()
                y= 750
            pdf.setFont("Helvetica", 7)    
            detalle_item.wrapOn(pdf, 300, 800)
            detalle_item.drawOn(pdf, 20,y)
                
            encabezados =('Mes','Inv.Inic','Valor','Entradas','Valor','Salidas','Valor','Inv.Final','Valor')
            detalle = [('Enero','{:,}'.format(acum.ii_01),'{:,}'.format(acum.ii_01*acum.costo_prom),'{:,}'.format(acum.ent_01),'{:,}'.format(acum.ent_01*acum.costo_prom),'{:,}'.format(acum.sal_01),'{:,}'.format(acum.sal_01*acum.costo_prom),'{:,}'.format(acum.if_01),'{:,}'.format(acum.if_01*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Febrero','{:,}'.format(acum.ii_02),'{:,}'.format(acum.ii_02*acum.costo_prom),'{:,}'.format(acum.ent_02),'{:,}'.format(acum.ent_02*acum.costo_prom),'{:,}'.format(acum.sal_02),'{:,}'.format(acum.sal_02*acum.costo_prom),'{:,}'.format(acum.if_02),'{:,}'.format(acum.if_02*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Marzo','{:,}'.format(acum.ii_03),'{:,}'.format(acum.ii_02*acum.costo_prom),'{:,}'.format(acum.ent_03),'{:,}'.format(acum.ent_03*acum.costo_prom),'{:,}'.format(acum.sal_03),'{:,}'.format(acum.sal_03*acum.costo_prom),'{:,}'.format(acum.if_03),'{:,}'.format(acum.if_03*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Abril','{:,}'.format(acum.ii_04),'{:,}'.format(acum.ii_04*acum.costo_prom),'{:,}'.format(acum.ent_04),'{:,}'.format(acum.ent_04*acum.costo_prom),'{:,}'.format(acum.sal_04),'{:,}'.format(acum.sal_04*acum.costo_prom),'{:,}'.format(acum.if_04),'{:,}'.format(acum.if_04*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Mayo','{:,}'.format(acum.ii_05),'{:,}'.format(acum.ii_05*acum.costo_prom),'{:,}'.format(acum.ent_05),'{:,}'.format(acum.ent_05*acum.costo_prom),'{:,}'.format(acum.sal_05),'{:,}'.format(acum.sal_05*acum.costo_prom),'{:,}'.format(acum.if_05),'{:,}'.format(acum.if_05*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Junio','{:,}'.format(acum.ii_06),'{:,}'.format(acum.ii_06*acum.costo_prom),'{:,}'.format(acum.ent_06),'{:,}'.format(acum.ent_06*acum.costo_prom),'{:,}'.format(acum.sal_06),'{:,}'.format(acum.sal_06*acum.costo_prom),'{:,}'.format(acum.if_06),'{:,}'.format(acum.if_06*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Julio','{:,}'.format(acum.ii_07),'{:,}'.format(acum.ii_07*acum.costo_prom),'{:,}'.format(acum.ent_07),'{:,}'.format(acum.ent_07*acum.costo_prom),'{:,}'.format(acum.sal_07),'{:,}'.format(acum.sal_07*acum.costo_prom),'{:,}'.format(acum.if_07),'{:,}'.format(acum.if_03*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Agosto','{:,}'.format(acum.ii_08),'{:,}'.format(acum.ii_08*acum.costo_prom),'{:,}'.format(acum.ent_08),'{:,}'.format(acum.ent_08*acum.costo_prom),'{:,}'.format(acum.sal_08),'{:,}'.format(acum.sal_08*acum.costo_prom),'{:,}'.format(acum.if_08),'{:,}'.format(acum.if_08*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Septiembre','{:,}'.format(acum.ii_09),'{:,}'.format(acum.ii_09*acum.costo_prom),'{:,}'.format(acum.ent_09),'{:,}'.format(acum.ent_09*acum.costo_prom),'{:,}'.format(acum.sal_09),'{:,}'.format(acum.sal_09*acum.costo_prom),'{:,}'.format(acum.if_09),'{:,}'.format(acum.if_09*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Octubre','{:,}'.format(acum.ii_10),'{:,}'.format(acum.ii_10*acum.costo_prom),'{:,}'.format(acum.ent_10),'{:,}'.format(acum.ent_10*acum.costo_prom),'{:,}'.format(acum.sal_10),'{:,}'.format(acum.sal_10*acum.costo_prom),'{:,}'.format(acum.if_10),'{:,}'.format(acum.if_10*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Noviembre','{:,}'.format(acum.ii_11),'{:,}'.format(acum.ii_11*acum.costo_prom),'{:,}'.format(acum.ent_11),'{:,}'.format(acum.ent_11*acum.costo_prom),'{:,}'.format(acum.sal_11),'{:,}'.format(acum.sal_11*acum.costo_prom),'{:,}'.format(acum.if_11),'{:,}'.format(acum.if_11*acum.costo_prom)) for acum in acumulados]
            detalle = detalle + [('Diciembre','{:,}'.format(acum.ii_12),'{:,}'.format(acum.ii_12*acum.costo_prom),'{:,}'.format(acum.ent_12),'{:,}'.format(acum.ent_12*acum.costo_prom),'{:,}'.format(acum.sal_12),'{:,}'.format(acum.sal_12*acum.costo_prom),'{:,}'.format(acum.if_12),'{:,}'.format(acum.if_12*acum.costo_prom)) for acum in acumulados]
            detalle_item = Table([encabezados] + detalle, colWidths=[2 * cm,2 * cm,2 * cm,2 * cm,2 * cm,2 * cm,2 * cm,2 * cm,2 * cm])
            detalle_item.setStyle(TableStyle(
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
            y = y - b*20
            if y<= 10:
                pdf.showPage()
                y= 600
            pdf.setFont("Helvetica", 7)    
            detalle_item.wrapOn(pdf, 300, 800)
            detalle_item.drawOn(pdf, 20,y)
            y -=20                         
        pdf.setFont("Helvetica", 9)
        pdf.drawString(240, y, u"Total Bodega      : "+('{:,}'.format(total_bodega)))    
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionAcumuladosInventarioXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    items = MaestroItem.objects.filter(acumula=True)
    bodegas = Bodega.objects.all()
    n = 2
    for bodega in bodegas:
        for item in items:
            #acum = AcumuladoItem.objects.filter(IdBodega_id=bodega.id)
            if request.session['items_acumulado_filtro']:
                lista_filtro = request.session['items_acumulado_filtro']
                acumulados = AcumuladoItem.objects.filter(IdBodega_id=bodega.id,IdItem_id=item.id,id__in=lista_filtro)
            else:    
                acumulados = AcumuladoItem.objects.filter(IdBodega_id=bodega.id,IdItem_id=item.id)
            sw = 0    
            for acum in acumulados:
                worksheet.write('A1','Descripcion')
                worksheet.write('B1','Costo Prom.')
                worksheet.write('C1','Cant. Max.')
                worksheet.write('D1','Cant. Min.')
                nn = str(n)
                exec("worksheet.write('A"+nn+"','"+acum.IdItem.descripcion+"' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.costo_prom)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.cant_maxima)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.cant_minima)+"' )")    
                n += 1
                nn = str(n)
                if sw == 0:
                    exec("worksheet.write('A"+nn+"','Mes' )")
                    exec("worksheet.write('B"+nn+"','Inv.Inic' )")    
                    exec("worksheet.write('C"+nn+"','Valor' )")
                    exec("worksheet.write('D"+nn+"','Entradas' )")
                    exec("worksheet.write('D"+nn+"','Valor' )")
                    exec("worksheet.write('E"+nn+"','Salidas' )")
                    exec("worksheet.write('F"+nn+"','Valor' )")
                    exec("worksheet.write('G"+nn+"','Inv.Final' )")
                    exec("worksheet.write('H"+nn+"','Valor' )")  
                    n +=1
                    nn = str(n)
                    sw = 1
                exec("worksheet.write('A"+nn+"','Enero' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_01)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_01*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_01)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_01*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_01)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_01*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_01)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_01*acum.costo_prom)+"' )")
                n +=1
                nn = str(n)
                exec("worksheet.write('A"+nn+"','Febrero' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_02)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_02*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_02)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_02*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_02)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_02*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_02)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_02*acum.costo_prom)+"' )")
                n +=1
                nn = str(n)
                exec("worksheet.write('A"+nn+"','Marzo' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_03)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_03*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_03)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_03*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_03)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_03*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_03)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_03*acum.costo_prom)+"' )")
                n +=1
                nn = str(n)
                exec("worksheet.write('A"+nn+"','Abril' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_04)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_04*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_04)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_04*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_04)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_04*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_04)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_04*acum.costo_prom)+"' )")
                n +=1
                nn = str(n)
                exec("worksheet.write('A"+nn+"','Mayo' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_05)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_05*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_05)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_05*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_05)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_05*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_05)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_02*acum.costo_prom)+"' )")
                n +=1
                nn = str(n)
                exec("worksheet.write('A"+nn+"','Junio' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_06)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_06*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_06)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_06*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_06)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_06*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_06)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_06*acum.costo_prom)+"' )")
                n +=1
                nn = str(n)
                exec("worksheet.write('A"+nn+"','Julio' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_07)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_07*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_07)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_07*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_07)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_07*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_07)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_07*acum.costo_prom)+"' )")
                n +=1
                nn = str(n)
                exec("worksheet.write('A"+nn+"','Agosto' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_08)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_08*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_08)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_08*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_08)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_08*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_08)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_08*acum.costo_prom)+"' )")
                n +=1
                nn = str(n)
                exec("worksheet.write('A"+nn+"','Septiembre' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_09)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_09*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_09)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_09*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_09)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_09*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_09)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_09*acum.costo_prom)+"' )")
                n +=1
                nn = str(n)
                exec("worksheet.write('A"+nn+"','Octubre' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_10)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_10*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_10)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_10*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_10)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_10*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_10)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_10*acum.costo_prom)+"' )")
                n +=1
                nn = str(n)
                exec("worksheet.write('A"+nn+"','Noviembre' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_11)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_11*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_11)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_11*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_11)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_11*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_11)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_11*acum.costo_prom)+"' )")
                n +=1
                nn = str(n)
                exec("worksheet.write('A"+nn+"','Diciembre' )")
                exec("worksheet.write('B"+nn+"','"+str(acum.ii_12)+"' )")    
                exec("worksheet.write('C"+nn+"','"+str(acum.ii_12*acum.costo_prom)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_12)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(acum.ent_12*acum.costo_prom)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(acum.sal_12)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(acum.sal_12*acum.costo_prom)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(acum.if_12)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(acum.if_12*acum.costo_prom)+"' )")
                n +=1
    workbook.close()
    output.seek(0)
    filename = 'acumulados_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response        

def ImpresionAcumuladosInventarioXlsUnItemView(request,iditem):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    items = MaestroItem.objects.filter(acumula=True,id=iditem)
    idbodega = request.session['idbodega']
    bodega = Bodega.objects.get(id=idbodega)
    n = 3
    for item in items:
        #acum = AcumuladoItem.objects.filter(IdBodega_id=bodega.id)
        if request.session['items_acumulado_filtro']:
            lista_filtro = request.session['items_acumulado_filtro']
            acumulados = AcumuladoItem.objects.filter(IdBodega_id=bodega.id,IdItem_id=item.id,id__in=lista_filtro)
        else:    
            acumulados = AcumuladoItem.objects.filter(IdBodega_id=bodega.id,IdItem_id=item.id)
        sw = 0 
        worksheet.write('A1','Bodega: '+bodega.descripcion)   
        for acum in acumulados:
            worksheet.write('A2','Descripcion')
            worksheet.write('B2','Costo Prom.')
            worksheet.write('C2','Cant. Max.')
            worksheet.write('D2','Cant. Min.')
            nn = str(n)
            exec("worksheet.write('A"+nn+"','"+acum.IdItem.descripcion+"' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.costo_prom)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.cant_maxima)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.cant_minima)+"' )")    
            n += 1
            nn = str(n)
            if sw == 0:
                exec("worksheet.write('A"+nn+"','Mes' )")
                exec("worksheet.write('B"+nn+"','Inv.Inic' )")    
                exec("worksheet.write('C"+nn+"','Valor' )")
                exec("worksheet.write('D"+nn+"','Entradas' )")
                exec("worksheet.write('D"+nn+"','Valor' )")
                exec("worksheet.write('E"+nn+"','Salidas' )")
                exec("worksheet.write('F"+nn+"','Valor' )")
                exec("worksheet.write('G"+nn+"','Inv.Final' )")
                exec("worksheet.write('H"+nn+"','Valor' )")  
                n +=1
                nn = str(n)
                sw = 1
            exec("worksheet.write('A"+nn+"','Enero' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_01)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_01*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_01)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_01*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_01)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_01*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_01)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_01*acum.costo_prom)+"' )")
            n +=1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','Febrero' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_02)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_02*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_02)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_02*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_02)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_02*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_02)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_02*acum.costo_prom)+"' )")
            n +=1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','Marzo' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_03)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_03*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_03)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_03*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_03)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_03*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_03)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_03*acum.costo_prom)+"' )")
            n +=1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','Abril' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_04)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_04*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_04)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_04*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_04)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_04*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_04)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_04*acum.costo_prom)+"' )")
            n +=1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','Mayo' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_05)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_05*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_05)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_05*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_05)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_05*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_05)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_02*acum.costo_prom)+"' )")
            n +=1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','Junio' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_06)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_06*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_06)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_06*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_06)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_06*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_06)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_06*acum.costo_prom)+"' )")
            n +=1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','Julio' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_07)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_07*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_07)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_07*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_07)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_07*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_07)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_07*acum.costo_prom)+"' )")
            n +=1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','Agosto' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_08)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_08*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_08)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_08*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_08)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_08*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_08)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_08*acum.costo_prom)+"' )")
            n +=1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','Septiembre' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_09)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_09*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_09)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_09*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_09)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_09*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_09)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_09*acum.costo_prom)+"' )")
            n +=1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','Octubre' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_10)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_10*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_10)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_10*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_10)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_10*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_10)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_10*acum.costo_prom)+"' )")
            n +=1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','Noviembre' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_11)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_11*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_11)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_11*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_11)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_11*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_11)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_11*acum.costo_prom)+"' )")
            n +=1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','Diciembre' )")
            exec("worksheet.write('B"+nn+"','"+str(acum.ii_12)+"' )")    
            exec("worksheet.write('C"+nn+"','"+str(acum.ii_12*acum.costo_prom)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_12)+"' )")
            exec("worksheet.write('D"+nn+"','"+str(acum.ent_12*acum.costo_prom)+"' )")
            exec("worksheet.write('E"+nn+"','"+str(acum.sal_12)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(acum.sal_12*acum.costo_prom)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(acum.if_12)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(acum.if_12*acum.costo_prom)+"' )")
            n +=1
    workbook.close()
    output.seek(0)
    filename = 'acumulados_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response

def ImpresionKardexInventarioView(request):
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
    pdf.drawString(200, y, u"KARDEX INVENTARIO")
    pdf.setFont("Helvetica", 9)
    kardex = Kardex.objects.all()
    pdf.setFont("Helvetica", 9)
    for n in kardex:
        descripcion = n.IdItem.descripcion
    y -= 20
    pdf.drawString(20, y, u"Item :"+descripcion)
    y -= 10
    encabezados =('Fecha','Número','Tipo Docum.','Factura','Ord.Compra','Pedido Caja','Valor','Cantidad','Valor Total','Saldo','Tipo Movim.')
    detalle = [(kardex.fecha,kardex.numero,kardex.IdTipoDocumento.descripcion[0:16],kardex.factura_compra,kardex.orden_compra,kardex.pedido_caja,'{:,}'.format(kardex.valor),'{:,}'.format(kardex.cantidad),'{:,}'.format(kardex.valor_total),'{:,}'.format(kardex.saldo),kardex.tipo_mov) for kardex in kardex]
    detalle_kardex = Table([encabezados] + detalle, colWidths=[1.8 * cm,1.8 * cm,2.3 * cm,1.6 * cm,1.6 * cm,1.9 * cm,2.3 * cm,1.6 * cm,1.8 * cm,1.6 * cm,1.8 * cm,1.8 * cm])
    detalle_kardex.setStyle(TableStyle(
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
    y = y - b*25
    if y<= 35:
        pdf.showPage()
        y= 750
    pdf.setFont("Helvetica", 7)    
    detalle_kardex.wrapOn(pdf, 300, 800)
    detalle_kardex.drawOn(pdf, 20,y)
    y -= 10
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionKardexInventarioXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
        
    worksheet.write('A1','Fecha' )
    worksheet.write('B1','Número' )
    worksheet.write('C1','Tipo Docum.')
    worksheet.write('D1','Pedido Caja')
    worksheet.write('E1','Factura Compra')
    worksheet.write('F1','Item')
    worksheet.write('G1','Valor')
    worksheet.write('H1','Cantidad')
    worksheet.write('I1','Valor Total')
    worksheet.write('J1','Saldo')
    worksheet.write('K1','Tipo Movim.')
    kardex = Kardex.objects.all()
    n=2
    for kardex in kardex:
        nn = str(n)
        exec("worksheet.write('A"+nn+"','"+kardex.fecha.strftime("%d/%m/%Y")+"' )")
        exec("worksheet.write('B"+nn+"','"+kardex.numero+"' )")
        exec("worksheet.write('C"+nn+"','"+kardex.IdTipoDocumento.descripcion+"' )")
        exec("worksheet.write('D"+nn+"','"+kardex.pedido_caja+"' )")
        exec("worksheet.write('E"+nn+"','"+kardex.factura_compra+"' )")
        exec("worksheet.write('F"+nn+"','"+kardex.IdItem.descripcion+"' )")
        exec("worksheet.write('G"+nn+"','"+str(kardex.valor)+"' )")
        exec("worksheet.write('H"+nn+"','"+str(kardex.cantidad)+"' )")
        exec("worksheet.write('I"+nn+"','"+str(kardex.valor_total)+"' )")
        exec("worksheet.write('J"+nn+"','"+str(kardex.saldo)+"' )")
        exec("worksheet.write('K"+nn+"','"+kardex.tipo_mov+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'kardex_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response    

def ImpresionEntradasInventarioView(request):
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
    pdf.drawString(200, y, u"ENTRADAS INVENTARIO")
    pdf.setFont("Helvetica", 9)
    y -= 50
    sw = 0
    if request.session['filtro_identradas']:
        identradas = request.session['filtro_identradas']
        entradas = Entrada.objects.filter(id__in=identradas)
    else:    
        entradas = Entrada.objects.all()
    for entrada in entradas:
        encabezados =('Fecha','Número','Tipo Docum.','Proveedor','Fact.Compra','Orden Compra','Despacho','Detalle','Valor')
        detalle = [(entrada.fecha,entrada.numero,entrada.IdTipoDocumento,entrada.IdProveedor.apenom[0:25],entrada.factura_compra,entrada.orden_compra,entrada.despacho,entrada.detalle,'{:,}'.format(entrada.valor))]
        detalle_entrada = Table([encabezados] + detalle, colWidths=[1.5 * cm,1.5 * cm,2.5 * cm,4 * cm,2.0 * cm,1.8 * cm,2.0 * cm,2 * cm])
        detalle_entrada.setStyle(TableStyle(
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
        detalle_entrada.wrapOn(pdf, 300, 800)
        detalle_entrada.drawOn(pdf, 20,y)
        y -= 20
    
        entrada_detalle = EntradaDetalle.objects.filter(numero=entrada.numero)
        encabezados =('Item','Cantidad','Valor','Valor Total')
        detalle = [(entdet.IdItem,'{:,}'.format(entdet.cantidad),'{:,}'.format(entdet.valor),'{:,}'.format(entdet.valor_total)) for entdet in entrada_detalle]
        detalle_entdet = Table([encabezados] + detalle, colWidths=[8 * cm,2.0 * cm,2.0 * cm,2.5 * cm])
        detalle_entdet.setStyle(TableStyle(
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
        detalle_entdet.wrapOn(pdf, 300, 800)
        detalle_entdet.drawOn(pdf, 20,y)
        y -= 50
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionEntradasInventarioXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    if request.session['filtro_identradas']:
        identradas = request.session['filtro_identradas']
        entradas = Entrada.objects.filter(id__in=identradas)
    else:    
        entradas = Entrada.objects.all()
    n=1
    for entrada in entradas:
        nn = str(n)
        exec("worksheet.write('A"+nn+"','Fecha')" )
        exec("worksheet.write('B"+nn+"','Número')" )
        exec("worksheet.write('C"+nn+"','Tipo Docum.')")
        exec("worksheet.write('D"+nn+"','Proveedor')")
        exec("worksheet.write('E"+nn+"','Fact.Compra')")
        exec("worksheet.write('F"+nn+"','Orden Compra')")
        exec("worksheet.write('G"+nn+"','Despacho')")
        exec("worksheet.write('H"+nn+"','Detalle')")
        exec("worksheet.write('I"+nn+"','Valor')")     
        n = n+1
        nn = str(n)
        exec("worksheet.write('A"+nn+"','"+entrada.fecha.strftime("%d/%m/%Y")+"' )")
        exec("worksheet.write('B"+nn+"','"+entrada.numero+"' )")
        exec("worksheet.write('C"+nn+"','"+entrada.IdTipoDocumento.descripcion+"' )")
        exec("worksheet.write('D"+nn+"','"+entrada.IdProveedor.apenom+"' )")
        exec("worksheet.write('E"+nn+"','"+entrada.factura_compra+"' )")
        exec("worksheet.write('F"+nn+"','"+entrada.orden_compra+"' )")
        exec("worksheet.write('G"+nn+"','"+entrada.despacho+"' )")
        exec("worksheet.write('H"+nn+"','"+entrada.detalle+"' )")
        exec("worksheet.write('I"+nn+"','"+str(entrada.valor)+"' )")
        entrada_detalle = EntradaDetalle.objects.filter(numero=entrada.numero)
        n = n+1
        nn = str(n)
        exec("worksheet.write('A"+nn+"','Número')" )
        exec("worksheet.write('B"+nn+"','Tipo Docum.')")
        exec("worksheet.write('C"+nn+"','Estado')")
        exec("worksheet.write('D"+nn+"','Item')")
        exec("worksheet.write('E"+nn+"','Valor')")
        exec("worksheet.write('F"+nn+"','Cantidad')")
        exec("worksheet.write('G"+nn+"','Valor Total')")
        for detalle in entrada_detalle:
            n= n+1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','"+detalle.numero+"' )")
            exec("worksheet.write('B"+nn+"','"+detalle.IdTipoDocumento.descripcion+"' )")
            exec("worksheet.write('C"+nn+"','"+str(detalle.estado)+"' )")
            exec("worksheet.write('D"+nn+"','"+detalle.IdItem.descripcion+"' )")
            exec("worksheet.write('E"+nn+"','"+str(detalle.valor)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(detalle.cantidad)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(detalle.valor_total)+"' )")          
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'entradas_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response


def ImpresionSalidasInventarioView(request):
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
    pdf.drawString(200, y, u"SALIDAS INVENTARIO")
    pdf.setFont("Helvetica", 9)
    y -= 50
    sw = 0
    if request.session['filtro_idsalidas']:
        idsalidas = request.session['filtro_idsalidas']
        salidas = Salida.objects.filter(id__in=idsalidas)
    else:
        salidas = Salida.objects.all()
    for salida in salidas:
        encabezados =('Fecha','Número','Tipo Docum.','Pedido Caja','Detalle','Estado','Valor','Usuario')
        detalle = [(salida.fecha,salida.numero,salida.IdTipoDocumento,salida.pedido_caja,salida.detalle,salida.estado,'{:,}'.format(salida.valor),salida.IdUsuario)]
        detalle_salida = Table([encabezados] + detalle, colWidths=[1.5 * cm,1.5 * cm,2.5 * cm,1.5 * cm,4.0 * cm,1.2 * cm,2.0 * cm,2.0 * cm])
        detalle_salida.setStyle(TableStyle(
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
        detalle_salida.wrapOn(pdf, 300, 800)
        detalle_salida.drawOn(pdf, 20,y)
        y -= 20
        salida_detalle = SalidaDetalle.objects.filter(numero=salida.numero)
        encabezados =('Item','Cantidad','Valor','Valor Total','Bodega')
        detalle = [(saldet.IdItem,'{:,}'.format(saldet.cantidad),'{:,}'.format(saldet.valor),'{:,}'.format(saldet.valor_total),P(item.IdBodega.descripcion)) for saldet in salida_detalle]
        detalle_saldet = Table([encabezados] + detalle, colWidths=[8 * cm,2.0 * cm,2.0 * cm,2.5 * cm,3 * cm])
        detalle_saldet.setStyle(TableStyle(
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
        detalle_saldet.wrapOn(pdf, 300, 800)
        detalle_saldet.drawOn(pdf, 20,y)
        y -= 50
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionSalidasInventarioXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    if request.session['filtro_idsalidas']:
        idsalidas = request.session['filtro_idsalidas']
        salidas = Salida.objects.filter(id__in=idsalidas)
    else:    
        salidas = Salida.objects.all()
    n=1
    for salida in salidas:
        nn = str(n)
               
        exec("worksheet.write('A"+nn+"','Fecha')" )
        exec("worksheet.write('B"+nn+"','Número')" )
        exec("worksheet.write('C"+nn+"','Tipo Docum.')")
        exec("worksheet.write('D"+nn+"','Pedido Caja')")
        exec("worksheet.write('E"+nn+"','Detalle')")
        exec("worksheet.write('F"+nn+"','Valor')")     
        n = n+1
        nn = str(n)
        exec("worksheet.write('A"+nn+"','"+salida.fecha.strftime("%d/%m/%Y")+"' )")
        exec("worksheet.write('B"+nn+"','"+salida.numero+"' )")
        exec("worksheet.write('C"+nn+"','"+salida.IdTipoDocumento.descripcion+"' )")
        exec("worksheet.write('D"+nn+"','"+salida.pedido_caja+"' )")
        exec("worksheet.write('E"+nn+"','"+salida.detalle+"' )")
        exec("worksheet.write('F"+nn+"','"+str(salida.valor)+"' )")
        salida_detalle = SalidaDetalle.objects.filter(numero=salida.numero)
        n = n+1
        nn = str(n)
        
        exec("worksheet.write('A"+nn+"','Número')" )
        exec("worksheet.write('B"+nn+"','Tipo Docum.')")
        exec("worksheet.write('C"+nn+"','Estado')")
        exec("worksheet.write('D"+nn+"','Item')")
        exec("worksheet.write('E"+nn+"','Valor')")
        exec("worksheet.write('F"+nn+"','Cantidad')")
        exec("worksheet.write('G"+nn+"','Valor Total')")
        for detalle in salida_detalle:
            n= n+1
            nn = str(n)
            exec("worksheet.write('A"+nn+"','"+detalle.numero+"' )")
            exec("worksheet.write('B"+nn+"','"+detalle.IdTipoDocumento.descripcion+"' )")
            exec("worksheet.write('C"+nn+"','"+str(detalle.estado)+"' )")
            exec("worksheet.write('D"+nn+"','"+detalle.IdItem.descripcion+"' )")
            exec("worksheet.write('E"+nn+"','"+str(detalle.valor)+"' )")
            exec("worksheet.write('F"+nn+"','"+str(detalle.cantidad)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(detalle.valor_total)+"' )")          
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'salidas_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    return response

def ImpresionInventarioFisicoView(request):
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
    pdf.drawString(200, y, u"INVENTARIO FÍSICO")
    pdf.setFont("Helvetica", 9)
    y -= 40
    idbodega=request.session['idbodega']
    idanio = request.session['idanio']
    idmes = request.session['idmes']
    items = InventarioFisico.objects.filter(IdBodega_id=idbodega,IdAnio_id=idanio,IdMes_id=idmes)
    #iditems=[]
    #for i in items:
    #      iditems.append(i.id)
    #inventario_fisico = InventarioFisico.objects.filter(id__in=iditems )
    encabezados =('Descripcion','Bodega','Inv.Fisico','Stock','diferencia','Núm.Ajuste','Mes','Anio')
    detalle = [(item.IdItem.descripcion[0:40],item.IdBodega.descripcion[0:30],'{:,}'.format(item.inv_fis),'{:,}'.format(item.inv_acum),'{:,}'.format(item.diferencia),item.numero_ajuste,item.IdMes.descripcion,item.IdAnio.anio) for item in items]
    detalle_item = Table([encabezados] + detalle, colWidths=[5 * cm,3 * cm,1.5 * cm,1.5 * cm,1.5 * cm,2 * cm,1.5 * cm,1.5 * cm])
    detalle_item.setStyle(TableStyle(
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
    detalle_item.wrapOn(pdf, 300, 800)
    detalle_item.drawOn(pdf, 20,y)
    y -= 10
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionInventarioFisicoXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    n=2
    idbodega=request.session['idbodega']
    idanio = request.session['idanio']
    idmes = request.session['idmes']
    items = InventarioFisico.objects.filter(IdBodega_id=idbodega,IdAnio_id=idanio,IdMes_id=idmes)
    worksheet.write('A1','Descripción' )
    worksheet.write('B1','Bodega')
    worksheet.write('C1','Inv.Físico')
    worksheet.write('D1','Inv.Acum')
    worksheet.write('E1','Diferencia')
    worksheet.write('F1','Numero Ajuste')
    worksheet.write('G1','Mes')
    worksheet.write('H1','Año')
    for item in items:
        nn = str(n)
        exec("worksheet.write('A"+nn+"','"+item.IdItem.descripcion+"' )")
        exec("worksheet.write('B"+nn+"','"+item.IdBodega.descripcion+"' )")
        exec("worksheet.write('C"+nn+"','"+str(item.inv_fis)+"' )")
        exec("worksheet.write('D"+nn+"','"+str(item.inv_acum)+"' )")
        exec("worksheet.write('E"+nn+"','"+str(item.diferencia)+"' )")
        exec("worksheet.write('F"+nn+"','"+str(item.numero_ajuste)+"' )")
        anio = Anio.objects.get(id=item.IdAnio_id)
        mes = Mes.objects.get(id=item.IdMes_id)
        exec("worksheet.write('G"+nn+"','"+str(mes.descripcion)+"' )")
        exec("worksheet.write('H"+nn+"','"+str(anio.anio)+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'items_inventario.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    

def PoneAnioInventariosView(request):
    salidas = Salida.objects.all()
    for sale in salidas:
        year = sale.fecha.year
        Salida.objects.filter(id=sale.id).update(anio = year)

    entradas = Entrada.objects.all()
    for entra in entradas:
        year = entra.fecha.year
        Entrada.objects.filter(id=entra.id).update(anio = year)
    return redirect('menu_inventarios')

def TrasladoBodegasGruposItemView(request):
    grupos = Grupo.objects.all()
    for grupo in grupos:
        items = MaestroItem.objects.filter(IdGrupo_id=grupo.id)
        for item in items:
            MaestroItem.objects.filter(id=item.id).update(IdBodega_id=grupo.IdBodega_id)
    mensaje1 = "Proceso Terminado : "
    mensaje2 = ""
    mensaje3 = ""
    parametro = 4  
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
    return render(request, 'inventarios/mensaje_proceso_terminado.html', context)

def ValidaTrasladoBodegasGruposItemsview(request):
    mensaje1 = "Este Proceso pone las bodegas especificadas en los grupos, "
    mensaje2 = "a los items de ese grupo "
    mensaje3 = " "
    parametro = 1  
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
    return render(request, 'inventarios/mensaje_valida_pone_bodegas_grupos_items.html', context) 
    


