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

from django.conf import settings

from core. models import Empresa

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


from core.models import Tercero,Sucursal,ValorDefecto,TipoIdentificacion,Ciudad,Departamento,Pais
from core.forms import TerceroReciboCajaForm
from core.tables import TercerosListaTable,TercerosLista1Table
from core.filters import TerceroNombreFilter 
from caja.models import ReciboCaja,ReciboCajaDetalle,TipoEgresoCaja,Caja,EgresoCaja,TipoDocumentoCaja,SesionCaja,PedidoCaja,TipoIngresoCaja,PedidoCajaDetalle,PagoReciboCaja,TipoPagoReciboCaja
from caja.tables import RecibosCajaTable,RecibosCajaDetalleTable,PedidosCajaTable,PedidosCajaTableConsolidado,PedidosCajaDetalleTable,PagosCajaTable,CierreCajaTable
from caja.filters import RecibosCajaFilter,PedidosCajaFilter,PagosCajaFilter,PedidosCajaConsolidadoFilter
from caja.forms import ReciboCajaForm,SesionCajaForm,PedidoCajaForm,PedidoCajaDetalleForm,PagoReciboCajaForm,ReciboCajaManualForm
from hotel.tables import HabitacionesTable,HabitacionesConsolidadoTable
from hotel.models import Habitacion,RegistroHotel
from restaurante.models import Mesa
from restaurante.tables import MesasTable
from inventarios.models import MaestroItem,Salida,TipoDocumentoInv,AcumuladoItem,SalidaDetalle
from inventarios.filters import MaestroItemsFilter
from inventarios.tables import ItemsListaTable,Bodega,ItemsListaPedidoTable
from inventarios  import views as InventariosView
from cocina.models import Receta,RecetaIngrediente,Ingrediente  

from django import forms

from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.humanize.templatetags.humanize import intcomma

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from  reportlab.lib.styles import ParagraphStyle
style = getSampleStyleSheet()['Normal']

# Create your views here.

""" def ActualizaAcumuladosInventarios(iditem,cantidad,mes,anio,topera):
    entradas = 0
    salidas = 0
    bodega_defecto = ValorDefecto.objects.get(idValor='05')
    bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
    sanio = str(anio)
    smes = mes
    cantidad = int(cantidad)
    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id)
    if smes == 1:
        inv_inic = acumulado.ii_01
        entradas = acumulado.ent_01
        salidas = acumulado.sal_01
        #inv_fin = acumulado.if_01
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_01=salidas,if_01=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_01=entradas,if_01=inv_final)
    if smes == 2:
        inv_inic = acumulado.if_01
        entradas = acumulado.ent_02
        salidas = acumulado.sal_02
        #inv_fialn = acumulado.if_02
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_02=salidas,ii_02=inv_inic,if_02=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_02=entradas,ii_02=inv_inic,if_02=inv_final)
        
    if smes == 3:
        inv_inic = acumulado.if_02
        entradas = acumulado.ent_03
        salidas = acumulado.sal_03
        #inv_final = acumulado.if_03
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_03=salidas,ii_03=inv_inic,if_03=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_03=entradas,ii_03=inv_inic,if_03=inv_final)
    if smes == 4:
        inv_inic = acumulado.if_03
        entradas = acumulado.ent_04
        salidas = acumulado.sal_04
        #inv_final = acumulado.if_04
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_04=salidas,ii_04=inv_inic,if_04=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_04=entradas,ii_04=inv_inic,if_04=inv_final)
    if smes == 5:
        inv_inic = acumulado.if_04
        entradas = acumulado.ent_05
        salidas = acumulado.sal_05
        #inv_final = acumulado.if_05
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_05=salidas,ii_05=inv_inic,if_05=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_05=entradas,ii_05=inv_inic,if_05=inv_final)
    if smes == 6:
        inv_inic = acumulado.if_05
        entradas = acumulado.ent_06
        salidas = acumulado.sal_06
        #inv_final = acumulado.if_06
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_06=salidas,ii_06=inv_inic,if_06=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_06=entradas,ii_06=inv_inic,if_06=inv_final)
    if smes == 7:
        inv_inic = acumulado.if_06
        entradas = acumulado.ent_07
        salidas = acumulado.sal_07
        #inv_final = acumulado.if_07
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_07=salidas,ii_07=inv_inic,if_07=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_07=entradas,ii_07=inv_inic,if_07=inv_final)
    if smes == 8:
        inv_inic = acumulado.if_07
        entradas = acumulado.ent_08
        salidas = acumulado.sal_08
        #inv_final = acumulado.if_08                    
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_08=salidas,ii_08=inv_inic,if_08=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_08=entradas,ii_08=inv_inic,if_08=inv_final)
    if smes == 9:
        inv_inic = acumulado.if_08
        entradas = acumulado.ent_09
        salidas = acumulado.sal_09
        #inv_final = acumulado.if_09
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_09=salidas,ii_09=inv_inic,if_09=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_09=entradas,ii_09=inv_inic,if_09=inv_final)
    if smes == 10:
        inv_inic = acumulado.ii_09
        entradas = acumulado.ent_10
        salidas = acumulado.sal_10
        #inv_final = acumulado.if_10
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_10=salidas,ii_10=inv_inic,if_10=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_10=entradas,ii_10=inv_inic,if_10=inv_final)
    if smes == 11:
        inv_inic = acumulado.ii_10
        entradas = acumulado.ent_11
        salidas = acumulado.sal_11
        #inv_final = acumulado.if_11
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_11=salidas,ii_11=inv_inic,if_11=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_11=entradas,ii_11=inv_inic,if_11=inv_final)
    if smes == 12:
        inv_inic = acumulado.ii_11
        entradas = acumulado.ent_12
        salidas = acumulado.sal_12
        #inv_final = acumulado.if_12
        if topera =='salida':
            salidas = salidas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_12=salidas,ii_12=inv_inic,if_12=inv_final)
        else:
            entradas = entradas+cantidad
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ent_12=entradas,ii_12=inv_inic,if_12=inv_final)
     
    
    x = range(1,13)    
    for i in x:
        acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id)    
        if i == 1:
            inv_inic = acumulado.ii_01
            entradas = acumulado.ent_01
            salidas = acumulado.sal_01
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(if_01=inv_final)
        if i == 2:
            inv_inic = acumulado.if_01
            entradas = acumulado.ent_02
            salidas = acumulado.sal_02
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_02=inv_inic,if_02=inv_final)
        if i == 3:
            inv_inic = acumulado.if_02
            entradas = acumulado.ent_03
            salidas = acumulado.sal_03
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_03=inv_inic,if_03=inv_final)
        if i == 4:
            inv_inic = acumulado.if_03
            entradas = acumulado.ent_04
            salidas = acumulado.sal_04
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_04=inv_inic,if_04=inv_final)
        if i == 5:
            inv_inic = acumulado.if_04
            entradas = acumulado.ent_05
            salidas = acumulado.sal_05
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_05=inv_inic,if_05=inv_final)
        if i == 6:
            acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id) 
            inv_inic = acumulado.if_05
            entradas = acumulado.ent_06
            salidas = acumulado.sal_06
            inv_final = inv_inic+entradas-salidas
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_06=inv_inic,if_06=inv_final)
        if i == 7:
            acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id) 
            inv_inic = acumulado.if_06
            entradas = acumulado.ent_07
            salidas = acumulado.sal_07
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_07=inv_inic,if_07=inv_final)
        if i == 8:
            inv_inic = acumulado.if_07
            entradas = acumulado.ent_08
            salidas = acumulado.sal_08
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_08=inv_inic,if_08=inv_final)
        if i == 9:
            inv_inic = acumulado.if_08
            entradas = acumulado.ent_09
            salidas = acumulado.sal_09
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_09=inv_inic,if_09=inv_final) 
        if i == 10:
            inv_inic = acumulado.if_09
            entradas = acumulado.ent_10
            salidas = acumulado.sal_10
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_10=inv_inic,if_10=inv_final)
        if i == 11:
            inv_inic = acumulado.if_10
            entradas = acumulado.ent_11
            salidas = acumulado.sal_11
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_11=inv_inic,if_11=inv_final)
        if i == 12:
            inv_inic = acumulado.if_11
            entradas = acumulado.ent_12
            salidas = acumulado.sal_12
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_12=inv_inic,if_12=inv_final) """

""" def ReversaAcumuladosInventarios(iditem,cantidad,mes,anio):
    entradas = 0
    salidas = 0
    bodega_defecto = ValorDefecto.objects.get(idValor='05')
    bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
    sanio = str(anio)
    smes = mes
    cantidad = int(cantidad)
    acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id)
    if smes == 1:
        nueva_sal = acumulado.sal_01 - cantidad
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_01=nueva_sal)
    if smes == 2:
        nueva_sal = acumulado.sal_02 - cantidad
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_02=nueva_sal)
    if smes == 3:
        salidas_ant = acumulado.sal_03
        nueva_sal = acumulado.sal_03 - cantidad
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_03=nueva_sal)
    if smes == 4:
        salidas_ant = acumulado.sal_04
        nueva_sal = acumulado.sal_04 - cantidad
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_04=nueva_sal)
    if smes == 5:
        salidas_ant = acumulado.sal_05
        nueva_sal = acumulado.sal_05 - cantidad
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_05=nueva_sal)
    if smes == 6:
        salidas_ant = acumulado.sal_06
        nueva_sal = acumulado.sal_06 - cantidad
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_06=nueva_sal)
    if smes == 7:
        salidas_ant = acumulado.sal_07
        nueva_sal = acumulado.sal_07 - cantidad
        print('Nueva Sal :',nueva_sal)
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_07=nueva_sal)
        acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id)
        print('Acumulado :',acumulado.sal_07)
    if smes == 8:
        salidas_ant = acumulado.sal_08
        nueva_sal = acumulado.sal_08 - cantidad
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_08=nueva_sal)
    if smes == 9:
        salidas_ant = acumulado.sal_09
        nueva_sal = acumulado.sal_09 - cantidad
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_09=nueva_sal)
    if smes == 10:
        salidas_ant = acumulado.sal_10
        nueva_sal = acumulado.sal_10 - cantidad
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_10=nueva_sal)
    if smes == 11:
        salidas_ant = acumulado.sal_11
        nueva_sal = acumulado.sal_11 - cantidad
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_11=nueva_sal)
    if smes == 12:
        salidas_ant = acumulado.sal_12
        nueva_sal = acumulado.sal_12 - cantidad
        AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(sal_12=nueva_sal)
            
    x = range(1,13)    
    for i in x:
        acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id)    
        if i == 1:
            inv_inic = acumulado.ii_01
            entradas = acumulado.ent_01
            salidas = acumulado.sal_01
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(if_01=inv_final)
        if i == 2:
            inv_inic = acumulado.if_01
            entradas = acumulado.ent_02
            salidas = acumulado.sal_02
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_02=inv_inic,if_02=inv_final)
        if i == 3:
            inv_inic = acumulado.if_02
            entradas = acumulado.ent_03
            salidas = acumulado.sal_03
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_03=inv_inic,if_03=inv_final)
        if i == 4:
            inv_inic = acumulado.if_03
            entradas = acumulado.ent_04
            salidas = acumulado.sal_04
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_04=inv_inic,if_04=inv_final)
        if i == 5:
            inv_inic = acumulado.if_04
            entradas = acumulado.ent_05
            salidas = acumulado.sal_05
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_05=inv_inic,if_05=inv_final)
        if i == 6:
            acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id) 
            inv_inic = acumulado.if_05
            entradas = acumulado.ent_06
            salidas = acumulado.sal_06
            inv_final = inv_inic+entradas-salidas
            print('inv. Final:',inv_final)  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_06=inv_inic,if_06=inv_final)
        if i == 7:
            acumulado = AcumuladoItem.objects.get(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id) 
            inv_inic = acumulado.if_06
            entradas = acumulado.ent_07
            salidas = acumulado.sal_07
            inv_final = inv_inic+entradas-salidas  
            print('inv. Inic:',inv_inic)
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_07=inv_inic,if_07=inv_final)
        if i == 8:
            inv_inic = acumulado.if_07
            entradas = acumulado.ent_08
            salidas = acumulado.sal_08
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_08=inv_inic,if_08=inv_final)
        if i == 9:
            inv_inic = acumulado.if_08
            entradas = acumulado.ent_09
            salidas = acumulado.sal_09
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_09=inv_inic,if_09=inv_final) 
        if i == 10:
            inv_inic = acumulado.if_09
            entradas = acumulado.ent_10
            salidas = acumulado.sal_10
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_10=inv_inic,if_10=inv_final)
        if i == 11:
            inv_inic = acumulado.if_10
            entradas = acumulado.ent_11
            salidas = acumulado.sal_11
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_11=inv_inic,if_11=inv_final)
        if i == 12:
            inv_inic = acumulado.if_11
            entradas = acumulado.ent_12
            salidas = acumulado.sal_12
            inv_final = inv_inic+entradas-salidas  
            AcumuladoItem.objects.filter(IdItem_id=iditem,anio=sanio,IdBodega_id=bodega.id).update(ii_12=inv_inic,if_12=inv_final)
"""

def PoneCerosAcumuladosInventarios(sanio,idbodega):
    x = range(1,13)    
    for i in x:
        if i == 1:
            AcumuladoItem.objects.filter(anio=sanio,IdBodega_id=idbodega).update(ent_01=0,sal_01=0,if_01=0)
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
 
           
def CreaDocumentoSalidaInventariosCabeza(fecha,num_ped,idsucursal,idusuario):
    tipodocumentoinv = TipoDocumentoInv.objects.get(idTipo='04')
    anumero = tipodocumentoinv.actual +1
    pnumero = str(anumero).zfill(tipodocumentoinv.longitud)
    pnumero = (tipodocumentoinv.caracteres).strip()+pnumero
    salida_venta = Salida()
    salida_venta.numero = pnumero
    salida_venta.IdTipoDocumento_id = tipodocumentoinv.id
    salida_venta.fecha = fecha
    salida_venta.anio = fecha.year 
    salida_venta.detalle = 'Salida por venta '
    salida_venta.estado = True
    salida_venta.valor = 0
    #salida_venta.IdBodega_id = idbodega
    salida_venta.IdSucursal_id = idsucursal
    salida_venta.IdUsuario_id = idusuario
    salida_venta.pedido_caja = num_ped
    salida_venta.save()
    TipoDocumentoInv.objects.filter(idTipo='04').update(actual=anumero)
    
        
def CreaDocumentoSalidaInventariosCuerpo(num_ped,iditem,cantidad,valor_venta,valor_total,idPedido_detalle):
    tipodocumentoinv = TipoDocumentoInv.objects.get(idTipo='04')
    salida = Salida.objects.get(pedido_caja=num_ped)
    salida_detalle = SalidaDetalle()
    salida_detalle.numero = salida.numero
    salida_detalle.IdTipoDocumento_id = tipodocumentoinv.idTipo
    salida_detalle.IdSalida_id = salida.id
    salida_detalle.estado = True
    salida_detalle.IdItem_id = iditem
    salida_detalle.valor = valor_venta
    salida_detalle.cantidad = cantidad
    salida_detalle.valor_total = valor_total
    salida_detalle.pedido_detalle_id = idPedido_detalle
    item_bod = MaestroItem.objects.get(id=iditem)
    salida_detalle.IdBodega_id = item_bod.IdBodega_id
    salida_detalle.save()
    pedido = PedidoCaja.objects.get(numero=num_ped)
    year = pedido.fecha
    anio = year.year
    mes = year.month
    #bodega_defecto = ValorDefecto.objects.get(idValor='05')
    #bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
    item = MaestroItem.objects.get(id=iditem)
    invinic = False
    InventariosView.ActualizaAcumuladosInventarios(iditem,cantidad,0,mes,anio,'salida',0,invinic)
    valor_total = SalidaDetalle.objects.filter(numero=salida.numero).aggregate(Sum('valor_total'))['valor_total__sum']
    Salida.objects.filter(numero=salida.numero).update(valor=valor_total)
    #ActualizaAcumuladosInventarios(iditem,cantidad,mes,anio,'salida')
    #salida_detalle.id +=1

def AperturaCajaView(request):
    if request.method == 'POST':
        form = SesionCajaForm(request.POST, request.FILES)
        if form.is_valid():
            obj = SesionCaja()
            obj = form.save(commit=False)
            idcaja = request.POST.get('IdCaja', None) 
            if SesionCaja.objects.filter(IdCaja_id=idcaja,abierta=True).exists():
                sesion_caja = SesionCaja.objects.get(IdCaja_id=idcaja,abierta=True)
                caja = Caja.objects.get(id=idcaja)
                request.session['nombrecaja'] = caja.descripcion
                request.session['idcaja'] = idcaja
                mensaje1 = "La Caja No."+caja.descripcion
                mensaje2 = ",ya está abierta desde el "+sesion_caja.created.strftime("%m/%d/%Y, %H:%M:%S")
                mensaje3 = ",por : "+request.user.username
                parametro = 1  
                context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'parametro':parametro}
                return render(request, 'caja/mensaje_error_caja.html', context)      
            else:
                request.session['idcaja'] = idcaja
                valor_defecto = ValorDefecto.objects.get(idValor='01')
                sucursal = Sucursal.objects.get(idSucursal=valor_defecto.valor) 
                obj.IdSucursal_id = sucursal.id 
                obj.IdUsuario_id = request.user.id
                obj.abierta=True
                obj.save()
                return redirect('pedido_caja_lista')
        else:
            mensaje1 = "Error en Formulario"
            mensaje2 = ""
            mensaje3 = ""  
            parametro = 1
            context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,}
            return render(request, 'caja/mensaje_error_apertura_caja.html', context)
            return redirect('home')               
    else:
        form = SesionCajaForm()
    return render(request, 'caja/apertura_caja.html', {'form': form})


def AceptaCierreCajaView(request):
    id = request.session['idsesioncaja']
    SesionCaja.objects.filter(id=id).update(abierta=False)
    return redirect('menu_caja')

def NiegaCierreCajaView(request):
    return redirect('menu_caja')

def CierreCajaView(request,id):
    request.session['idsesioncaja'] = id
    mensaje1 = "Esta seguro de querer cerrar ésta Caja?"
    mensaje2 = ""
    mensaje3 = ""  
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3}
    return render(request, 'caja/mensaje_cierre_caja.html', context)

def IngresoCajaView(request,id):
    request.session['pedidostodos'] = False
    idcaja = id
    request.session['idcaja'] = idcaja
    return redirect('pedido_caja_lista')
   

def PedidoCajaListaView(request):
    #request.session['pedidostodos'] = False
    idcaja = request.session['idcaja']
    caja = Caja.objects.get(id=idcaja)
    if caja.consolidada:
        request.session['consolidar'] = True
        request.session['sel_item']= False
        #request.session['id_habitacion_consolidar'] = 0
        habitaciones = HabitacionesConsolidadoTable(Habitacion.objects.all())
        if request.session['pedidosconsolidados'] == True:
            idhabitacion = request.session['id_habitacion_consolidar']
            queryset = PedidoCaja.objects.filter(cerrado=False,IdHabitacion_id=idhabitacion).order_by('numero').reverse()
        else:        
            queryset = PedidoCaja.objects.filter(cerrado=False).order_by('numero').reverse()
        idpedidos_cons=[]
        f = PedidosCajaConsolidadoFilter(request.GET, queryset=queryset)
        for i in f.qs:
            idpedidos_cons.append(i.id)
            #request.session['id_habitacion_consolidar'] = i.IdHabitacion_id
            request.session['idhabitacion'] = i.IdHabitacion_id
            request.session['idpedidocaja'] = i.id
            idpedidos_cons.append(i.id)
        request.session['lista_id_filtro_pedido_caja']  = idpedidos_cons    
        total_pedidos = PedidoCaja.objects.filter(id__in=idpedidos_cons).aggregate(Sum('valor_total'))['valor_total__sum']     
        request.session['idpedidos_cons'] = idpedidos_cons
        pedidos_caja = PedidosCajaTableConsolidado(f.qs)
        nombre_caja = caja.descripcion
        pedidos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
        context = {'pedidos_caja':pedidos_caja,'filter':f,'nombre_caja':caja.descripcion,'total_pedidos':total_pedidos,'habitaciones':habitaciones}
        return render(request, 'caja/pedidos_caja_lista_consolidado.html', context)
    
    else:
        request.session['pedidosconsolidados'] = False
        request.session['consolidar'] = False
        print('Id Caja cuando entra: ',idcaja)
        #request.session['filtra_lista_pedidos'] = True
        idpedidos_cons=[]
        request.session['lista_id_filtro_pedido_caja']  = idpedidos_cons
    
        request.session['filtra_lista_pedidos'] = True
        request.session['sel_item']= False
        habitaciones = HabitacionesTable(Habitacion.objects.all())
        mesas = MesasTable(Mesa.objects.all())
        if SesionCaja.objects.filter(IdCaja_id=idcaja).exists():
            sesion_caja = SesionCaja.objects.get(IdCaja_id=idcaja,abierta=True)
            caja = Caja.objects.get(id=sesion_caja.IdCaja_id)
            queryset = PedidoCaja.objects.filter(IdCaja_id=idcaja,cerrado=False).order_by('numero').reverse()
            f = PedidosCajaFilter(request.GET, queryset=queryset)
            idpedidos_cons=[]
            for i in f.qs:
                idpedidos_cons.append(i.id)
            request.session['lista_id_filtro_pedido_caja']  = idpedidos_cons    
            total_pedidos = PedidoCaja.objects.filter(id__in=idpedidos_cons).aggregate(Sum('valor_total'))['valor_total__sum']  
            pedidos_caja = PedidosCajaTable(f.qs)
            pedidos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
            context = {'pedidos_caja':pedidos_caja,'filter':f,'nombre_caja':caja.descripcion,'habitaciones':habitaciones,'mesas':mesas,'total_pedidos':total_pedidos}
            return render(request, 'caja/pedidos_caja_lista.html', context)
    
    """ else:
        
        #sesion_caja = SesionCaja.objects.get(IdCaja_id=caja.id)
        #request.session['idcaja']=caja.id
        request.session['sel_item']= False
        #request.session['vaya_a_lista_pedidos']=False
        habitaciones = HabitacionesConsolidadoTable(Habitacion.objects.all())
        queryset = PedidoCaja.objects.filter(cerrado=False).order_by('numero').reverse()
        idpedidos_cons=[]
        f = PedidosCajaConsolidadoFilter(request.GET, queryset=queryset)
        #valor_total = 0
        for i in f.qs:
            idpedidos_cons.append(i.id)
            request.session['idhabitacion'] = i.IdHabitacion_id
            request.session['idpedidocaja'] = i.id
        request.session['lista_id_filtro_pedido_caja']  = idpedidos_cons    
        total_pedidos = PedidoCaja.objects.filter(id__in=idpedidos_cons).aggregate(Sum('valor_total'))['valor_total__sum']     
        request.session['idpedidos_cons'] = idpedidos_cons
        pedidos_caja = PedidosCajaTableConsolidado(f.qs)
        #nombre_caja = request.session['nombrecaja']
        nombre_caja = caja.descripcion
        pedidos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
        print('Id Caja cuando sale: ',id)
        context = {'pedidos_caja':pedidos_caja,'filter':f,'nombre_caja':caja.descripcion,'total_pedidos':total_pedidos,'habitaciones':habitaciones}
        return render(request, 'caja/pedidos_caja_lista_consolidado.html', context)   """
    """ else:
        if id == 98:
            caja = Caja.objects.get(idCaja='99')
            nombre_caja = caja.descripcion
            idpedidos_cons = request.session['idpedidos_cons']
            pedidos_caja = PedidoCaja.objects.filter(id__in=idpedidos_cons)
            total_pedidos = PedidoCaja.objects.filter(id__in=idpedidos_cons).aggregate(Sum('valor_total'))['valor_total__sum']
            f = PedidosCajaConsolidadoFilter(request.GET, queryset=pedidos_caja)
            pedidos_caja = PedidosCajaTableConsolidado(f.qs)
            pedidos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
            habitaciones = HabitacionesConsolidadoTable(Habitacion.objects.all())
            context = {'pedidos_caja':pedidos_caja,'filter':f,'nombre_caja':caja.descripcion,'total_pedidos':total_pedidos,'habitaciones':habitaciones}
            return render(request, 'caja/pedidos_caja_lista_consolidado.html', context) 
        if id == 0:
            id = request.session['idcaja']
        if SesionCaja.objects.filter(IdCaja_id=id,abierta=True).exists():    
            sesion_caja = SesionCaja.objects.get(IdCaja_id=id,abierta=True)
            caja = Caja.objects.get(id=sesion_caja.IdCaja_id)
        else:
            caja = Caja.objects.get(idCaja='99')    
        if caja.idCaja =='99':
            request.session['filtra_lista_pedidos'] = True
            request.session['idcaja']=id
            request.session['sel_item']= False
            request.session['vaya_a_lista_pedidos']=False
            habitaciones = HabitacionesConsolidadoTable(Habitacion.objects.all())
            queryset = PedidoCaja.objects.filter(cerrado=False).order_by('numero').reverse()
            idpedidos_cons=[]
            f = PedidosCajaConsolidadoFilter(request.GET, queryset=queryset)
            #valor_total = 0
            for i in f.qs:
                idpedidos_cons.append(i.id)
                request.session['idhabitacion'] = i.IdHabitacion_id
                request.session['idpedidocaja'] = i.id
            request.session['lista_id_filtro_pedido_caja']  = idpedidos_cons    
            total_pedidos = PedidoCaja.objects.filter(id__in=idpedidos_cons).aggregate(Sum('valor_total'))['valor_total__sum']       
            request.session['idpedidos_cons'] = idpedidos_cons
            pedidos_caja = PedidosCajaTableConsolidado(f.qs)
            #nombre_caja = request.session['nombrecaja']
            pedidos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
            context = {'pedidos_caja':pedidos_caja,'filter':f,'nombre_caja':caja.descripcion,'total_pedidos':total_pedidos,'habitaciones':habitaciones}
            return render(request, 'caja/pedidos_caja_lista_consolidado.html', context) 
        else:
            request.session['filtra_lista_pedidos'] = True
            request.session['idcaja']=id
            request.session['sel_item']= False
            request.session['vaya_a_lista_pedidos']=False
            habitaciones = HabitacionesTable(Habitacion.objects.all())
            mesas = MesasTable(Mesa.objects.all())
            sesion_caja = SesionCaja.objects.get(IdCaja_id=id,abierta=True)
            caja = Caja.objects.get(id=sesion_caja.IdCaja_id)
            idcaja = id
            queryset = PedidoCaja.objects.filter(IdCaja_id=idcaja,cerrado=False).order_by('numero').reverse()
            f = PedidosCajaFilter(request.GET, queryset=queryset)
            idpedidos_cons=[]
            for i in f.qs:
                idpedidos_cons.append(i.id)
            request.session['lista_id_filtro_pedido_caja']  = idpedidos_cons    
            total_pedidos = PedidoCaja.objects.filter(id__in=idpedidos_cons).aggregate(Sum('valor_total'))['valor_total__sum']  
            pedidos_caja = PedidosCajaTable(f.qs)
            #nombre_caja = request.session['nombrecaja']
            pedidos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
            context = {'pedidos_caja':pedidos_caja,'filter':f,'nombre_caja':caja.descripcion,'habitaciones':habitaciones,'mesas':mesas,'total_pedidos':total_pedidos}
            return render(request, 'caja/pedidos_caja_lista.html', context)
 """
def PedidoCajaListaTodosView(request):
    request.session['pedidostodos'] = True
    request.session['lista_id_filtro_pedido_caja'] = []
    queryset = PedidoCaja.objects.all().order_by('numero').reverse()
    #request.session['idpedidos_cons'] = ''
    idpedidos_cons=[]
    f = PedidosCajaConsolidadoFilter(request.GET, queryset=queryset)
    for i in f.qs:
        idpedidos_cons.append(i.id)
        request.session['idhabitacion'] = i.IdHabitacion_id
        request.session['idpedidocaja'] = i.id
    request.session['lista_id_filtro_pedido_caja']  = idpedidos_cons
    total_pedidos = PedidoCaja.objects.filter(id__in=idpedidos_cons).aggregate(Sum('valor_total'))['valor_total__sum']     
    pedidos_caja = PedidosCajaTable(f.qs)
    pedidos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
    descripcion = 'Todas'
    context = {'pedidos_caja':pedidos_caja,'filter':f,'nombre_caja':descripcion,'total_pedidos':total_pedidos}
    return render(request, 'caja/pedidos_caja_lista_todos.html', context)  



""" def ConsolidarPedidosCajaView(request,id):
    request.session['idcaja']=id
    request.session['sel_item']= False
    request.session['vaya_a_lista_pedidos']=False
    habitaciones = HabitacionesConsolidadoTable(Habitacion.objects.all())
    #mesas = MesasTable(Mesa.objects.all())
    sesion_caja = SesionCaja.objects.get(IdCaja_id=id,abierta=True)
    caja = Caja.objects.get(id=sesion_caja.IdCaja_id)
    idcaja = id
    queryset = PedidoCaja.objects.filter(IdCaja_id=idcaja,cerrado=False).order_by('fecha').reverse()
    f = PedidosCajaFilter(request.GET, queryset=queryset)
    idpedidos_cons=[]
    for i in f.qs:
        idpedidos_cons.append(i.id)
    total_pedidos = PedidoCaja.objects.filter(id__in=idpedidos_cons).aggregate(Sum('valor_total'))['valor_total__sum']  
    pedidos_caja = PedidosCajaTable(f.qs)
    #nombre_caja = request.session['nombrecaja']
    pedidos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
    context = {'pedidos_caja':pedidos_caja,'filter':f,'nombre_caja':caja.descripcion,'habitaciones':habitaciones,'mesas':mesas,'total_pedidos':total_pedidos}
    return render(request, 'caja/pedidos_caja_lista_consolidado.html', context)  """ 

def PedidosCajaConsolidadosView(request,id):
    idcaja=request.session['idcaja']
    #request.session['retorne_pedido_caja_consolidado'] = True
    request.session['id_habitacion_consolidar'] = id
    request.session['sel_item']= False
    request.session['pedidosconsolidados'] = True
    #request.session['vaya_a_lista_pedidos']=False
    habitaciones = HabitacionesConsolidadoTable(Habitacion.objects.all())
    mesas = MesasTable(Mesa.objects.all())
    #mesas = MesasTable(Mesa.objects.all())
    #sesion_caja = SesionCaja.objects.get(IdCaja_id=idcaja,abierta=True)
    #caja = Caja.objects.get(idCaja='99')
    pedidos = PedidoCaja.objects.filter(cerrado=False,IdHabitacion_id=id).order_by('numero').reverse()
    #queryset = PedidoCaja.objects.filter(cerrado=False,IdHabitacion_id=id).order_by('fecha').reverse()
    #f = PedidosCajaFilter(request.GET, queryset=queryset)
    idpedidos_cons=[]
    for i in pedidos:
        idpedidos_cons.append(i.id)
    request.session['id_pedidos_consolidados'] = idpedidos_cons
    request.session['consolidar'] = True    
    total_pedidos = PedidoCaja.objects.filter(id__in=idpedidos_cons).aggregate(Sum('valor_total'))['valor_total__sum']  
    pedidos_caja = PedidosCajaTableConsolidado(pedidos)
    caja = Caja.objects.get(id=idcaja)
    nombre_caja = caja.descripcion
    pedidos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
    context = {'pedidos_caja':pedidos_caja,'nombre_caja':caja.descripcion,'habitaciones':habitaciones,'mesas':mesas,'total_pedidos':total_pedidos}
    return render(request, 'caja/pedidos_caja_lista_consolidado.html', context) 
        
def CierrePedidoCajaConsolidadoView(request):
    if request.session['consolidar'] == True:
        return redirect('busca_tercero_cierre_pedido_caja_consolidado')
    else:
        mensaje1 = "Debe consolidar la cuenta, primero"
        mensaje2 = ''
        mensaje3 = ''
        return render(request,'caja/mensaje_error_consolidar_recibo_caja.html',{'mensaje1':mensaje1})

class BuscaTerceroCierrePedidoCajaConsolidadoView(SingleTableMixin,FilterView):
    table_class = TercerosLista1Table
    model = Tercero
    template_name = "core/terceros_caja_filter_consolidado.html"
    filterset_class = TerceroNombreFilter
    paginate_by = 8

class SeleccionaCajaReciboCajaConsolidadoView(TemplateView):
    template_name = "caja/selecciona_caja_cierre_consolidado.html"
      
def ReciboCajaConsolidadoView(request,id):
    #request.session['idcaja'] = id
    return redirect('selecciona_caja_recibo_caja_consolidado')

def CreaReciboCajaConsolidadoView(request,id):
    idCaja=id
    request.session['recibostodos'] = False
    request.session['consolidar'] = True    
    idtercero = request.session['idtercero']
    print('Tercero Id Caja:',idtercero)
    idhabitacion = request.session['id_habitacion_consolidar']
    idpedidocaja = request.session['idpedidocaja'] 
    mesa = Mesa.objects.get(idMesa = '*')
    sucursal_defecto = ValorDefecto.objects.get(idValor='01')
    sucursal =Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
    recibo_caja = ReciboCaja()
    tipodocumento = TipoDocumentoCaja.objects.get(idTipo='02')
    anumero = tipodocumento.actual +1
    snumero = str(anumero).zfill(tipodocumento.longitud)
    snumero = tipodocumento.caracteres+snumero
    recibo_caja.IdTipoDocumento_id = tipodocumento.id 
    recibo_caja.numero =  snumero
    recibo_caja.fecha = date.today()
    recibo_caja.estado = True
    recibo_caja.pedido_caja = 'Varios'
    recibo_caja.IdTercero_id = idtercero
    recibo_caja.IdMesa_id = mesa.id
    recibo_caja.IdHabitacion_id = idhabitacion
    recibo_caja.IdCaja_id = idCaja
    recibo_caja.IdSucursal_id = sucursal_defecto.id
    recibo_caja.IdUsuario_id = request.user.id
    recibo_caja.save()
    bodega_defecto = ValorDefecto.objects.get(idValor='05')
    bodega =Bodega.objects.get(idBodega=bodega_defecto.valor)
    idhabitacion_consolidar = request.session['id_habitacion_consolidar']
    pedidos = PedidoCaja.objects.filter(IdHabitacion_id=idhabitacion_consolidar,cerrado=False)
    for n in pedidos:
        PedidoCaja.objects.filter(numero=n.numero).update(cerrado=True,recibo_caja=snumero)
    TipoDocumentoCaja.objects.filter(idTipo='02').update(actual = anumero ) 
    recibo_caja = ReciboCaja.objects.get(numero=snumero)
    recibo_caja_detalle = ReciboCajaDetalle()
    tot_val_rec = 0
   
    #for n in idpedidos_cons:
    for n in pedidos:
        pedido_caja = PedidoCaja.objects.get(numero=n.numero)
        pedido_caja_detalle = PedidoCajaDetalle.objects.filter(numero=pedido_caja.numero)
        for ped in pedido_caja_detalle:
            recibo_caja_detalle.numero = snumero
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
    ReciboCaja.objects.filter(numero=snumero).update(valor=tot_val_rec)        
    return redirect('recibo_caja_detalle',recibo_caja.id) 

def PedidoCajaDetalleListaView(request,id):
    request.session['retorne_pedido_caja']=True
    request.session['vaya_a_lista_pedidos']= True
    request.session['idpedidocaja'] = id
    idcaja = request.session['idcaja']
    idpedido_caja = id
    pedido_caja = PedidoCaja.objects.get(id=idpedido_caja)
    caja = Caja.objects.get(id=pedido_caja.IdCaja_id)
    pedido_caja_table = PedidosCajaTable(PedidoCaja.objects.filter(id=idpedido_caja))
    pedido_detalle_caja = PedidosCajaDetalleTable(PedidoCajaDetalle.objects.filter(IdPedidoCaja_id=idpedido_caja))
    #total_pedidos = PedidoCaja.objects.filter(id=idpedido_caja).aggregate(Sum('valor_total'))['valor_total__sum']  
    context = {'pedido_detalle_caja':pedido_detalle_caja,'pedido_caja':pedido_caja_table,'idpedido':idpedido_caja,'nombre_caja':caja.descripcion,'valor_total':pedido_caja.valor_total,'idcaja':idcaja}
    return render(request, 'caja/pedidos_caja_detalle_lista.html', context) 

def CreaPedidoCajaMesaView(request,id):
    request.session['pedidostodos'] = False
    idcaja = request.session['idcaja']
    caja = Caja.objects.get(id=idcaja)
    mesa = Mesa.objects.get(id=id)
    habitacion = Habitacion.objects.get(idHabitacion='*')
    tipodocumento = TipoDocumentoCaja.objects.get(idTipo='01')
    tipoingreso = TipoIngresoCaja.objects.get(idTipoIngreso='01')
    sucursal_defecto = ValorDefecto.objects.get(idValor='01')
    sucursal =Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
    
    if PedidoCaja.objects.filter(IdMesa_id=id,IdCaja_id=idcaja,cerrado=False).exists():
        pedido_caja = PedidoCaja.objects.get(IdMesa_id=id,IdCaja_id=idcaja,cerrado=False)
        request.session['retorne_pedido_caja'] = True
        mensaje1 = "Ya existe un pedido abierto No. <"+pedido_caja.numero+">,para esa mesa:<"+pedido_caja.IdMesa.descripcion+">"
        mensaje2 = ''
        mensaje3 = ''
        return render(request,'caja/mensaje_error_apertura_caja.html',{'mensaje1':mensaje1})
    
    else:    
        anumero = tipodocumento.actual +1
        snumero = str(anumero).zfill(tipodocumento.longitud)
        snumero = tipodocumento.caracteres+snumero
        pedido_caja = PedidoCaja()
        pedido_caja.numero = snumero 
        pedido_caja.fecha = timezone.now()    
        pedido_caja.IdTipoingreso_id = tipoingreso.id 
        pedido_caja.recibo_caja=''
        pedido_caja.estado = True
        pedido_caja.IdTipodocumento_id=tipodocumento.id
        pedido_caja.IdMesa_id = mesa.id
        pedido_caja.IdHabitacion_id = habitacion.id
        pedido_caja.IdCaja_id = caja.id
        pedido_caja.IdSucursal_id = sucursal.id
        pedido_caja.IdUsuario_id = request.user.id
        pedido_caja.cerrado=False
        pedido_caja.save()
        #bodega_defecto = ValorDefecto.objects.get(idValor='05')
        #bodega =Bodega.objects.get(idBodega=bodega_defecto.valor)
        ########### Interfase Inventarios
        CreaDocumentoSalidaInventariosCabeza(date.today(),snumero,sucursal.id,request.user.id)
        #Mesa.objects.get(id=mesa.id).update(en_uso=True)
        TipoDocumentoCaja.objects.filter(idTipo='01').update(actual=anumero)
        idcaja = request.session['idcaja']
        pedido = PedidoCaja.objects.get(numero=snumero) 
        #return redirect('ingreso_caja',idcaja)
        return redirect('detalle_pedido_caja',pedido.id)

 

def CreaPedidoCajaHabitacionView(request,id):
    idcaja = request.session['idcaja']
    caja = Caja.objects.get(id=idcaja)
    mesa = Mesa.objects.get(idMesa='*')
    habitacion = Habitacion.objects.get(id=id)
    tipodocumento = TipoDocumentoCaja.objects.get(idTipo='01')
    tipoingreso = TipoIngresoCaja.objects.get(idTipoIngreso='01')
    sucursal_defecto = ValorDefecto.objects.get(idValor='01')
    sucursal =Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
    
    if PedidoCaja.objects.filter(IdHabitacion_id=id,IdCaja_id=idcaja,cerrado=False).exists():
        pedido_caja = PedidoCaja.objects.get(IdHabitacion_id=id,IdCaja_id=idcaja,cerrado=False)
        mensaje1 = "Ya existe un pedido abierto para esa habitacion "
        mensaje2 = 'Pedido No. '+pedido_caja.numero+' Fecha :'+str(pedido_caja.fecha)
        mensaje3 = ''
        return render(request,'caja/mensaje_error_pedido_caja.html',{'mensaje1':mensaje1,'mensaje2':mensaje2})
    else:
        anumero = tipodocumento.actual +1
        snumero = str(anumero).zfill(tipodocumento.longitud)
        snumero = tipodocumento.caracteres+snumero
        pedido_caja = PedidoCaja()
        pedido_caja.numero = snumero 
        pedido_caja.fecha = timezone.now()    
        pedido_caja.IdTipoingreso_id = tipoingreso.id 
        pedido_caja.recibo_caja=''
        pedido_caja.estado = True
        pedido_caja.IdTipodocumento_id=tipodocumento.id
        pedido_caja.IdMesa_id = mesa.id
        pedido_caja.IdHabitacion_id = habitacion.id
        pedido_caja.IdCaja_id = caja.id
        pedido_caja.IdSucursal_id = sucursal.id
        pedido_caja.IdUsuario_id = request.user.id
        pedido_caja.cerrado=False
        pedido_caja.save()
        #bodega_defecto = ValorDefecto.objects.get(idValor='05')
        #bodega =Bodega.objects.get(idBodega=bodega_defecto.valor)
        pedido = PedidoCaja.objects.get(numero=snumero)
        TipoDocumentoCaja.objects.filter(idTipo='01').update(actual=anumero)
        CreaDocumentoSalidaInventariosCabeza(date.today(),snumero,sucursal.id,request.user.id) 
        return redirect('detalle_pedido_caja',pedido.id)

def SeleccionaItemPedidoCajaView(request,id):
    request.session['idpedido'] = id
    return redirect(reverse('filtra_item_pedido_caja'))

class FiltraItemPedidoCajaView(SingleTableMixin, FilterView):
    table_class = ItemsListaPedidoTable
    model = MaestroItem
    template_name = "inventarios/items_inventario_filter.html"
    filterset_class = MaestroItemsFilter
    paginate_by = 8
    

def DescargaFormulaProducto(numero_ped,iditem,cantidad):
    if Receta.objects.filter(producto_id=iditem).exists():
        receta = Receta.objects.get(producto_id=iditem)
        pedido = PedidoCaja.objects.get(numero=numero_ped)
        ingredientes_receta = RecetaIngrediente.objects.filter(receta_id=receta.id)
        sucursal_defecto = ValorDefecto.objects.get(idValor='01')
        sucursal =Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
        idusuario = pedido.IdUsuario_id
        CreaDocumentoSalidaInventariosCabeza(date.today(),numero_ped,sucursal.id,idusuario)
        for i in ingredientes_receta:
            ingrediente = Ingrediente.objects.get(id=i.ingrediente_id)
            item = MaestroItem.objects.get(id=ingrediente.ingrediente_id)
            cantidad_necesaria = i.cantidad_necesaria * int(float(cantidad))
            CreaDocumentoSalidaInventariosCuerpo(numero_ped,item.id,cantidad_necesaria,0,0,0)
    return

def AdicionaItemPedido(iditem,cantidad,idpedido):
    detalle_pedido = PedidoCajaDetalle()
    item = MaestroItem.objects.get(id=iditem)
    pedido = PedidoCaja.objects.get(id=idpedido)        
    idtipodoc = TipoDocumentoCaja.objects.get(idTipo='01')
    detalle_pedido.numero = pedido.numero
    detalle_pedido.IdTipoDocumento_id = idtipodoc.id
    detalle_pedido.IdPedidoCaja_id = pedido.id
    detalle_pedido.IdItem_id = iditem
    detalle_pedido.valor = item.valor_venta
    detalle_pedido.cantidad = cantidad
    detalle_pedido.valor_total = item.valor_venta*int(float(cantidad))
    detalle_pedido.save()
    pedido_detalle =PedidoCajaDetalle.objects.filter(numero=pedido.numero)
    total = 0
    n = 0
    for ped_det in pedido_detalle:
        total = total + ped_det.valor_total
        n = n+1
    PedidoCaja.objects.filter(numero=pedido.numero).update(valor_total=total,total_items = n)
    #detalle_pedido_last = PedidoCajaDetalle.objects.latest('id')
    maestro_item = MaestroItem.objects.get(id=iditem)
    if maestro_item.acumula == True:
        print('entra')
        CreaDocumentoSalidaInventariosCuerpo(pedido.numero,iditem,cantidad,maestro_item.valor_venta,maestro_item.valor_venta*int(float(cantidad)),detalle_pedido.id)
    if (maestro_item.tipo_producto).strip() == 'PT':
        print('Entra 1')
        val_defecto = ValorDefecto.objects.get(idValor='11')
        if (val_defecto.valor).strip() == '1':
            print('entra2')
            DescargaFormulaProducto(pedido.numero,iditem,cantidad)
    pedido_detalle_regs = PedidoCajaDetalle.objects.filter(numero=pedido.numero)
    total=0
    items = 0
    tipodocumento = TipoDocumentoCaja.objects.get(idTipo='02')
    #recibo_caja = ReciboCaja.objects.get(numero=pedido.recibo_caja) 
    if ReciboCaja.objects.filter(numero=pedido.recibo_caja).exists():
        recibo_caja = ReciboCaja.objects.get(numero=pedido.recibo_caja)
        recibo_caja_detalle = ReciboCajaDetalle()
        recibo_caja_detalle.numero = pedido.recibo_caja
        recibo_caja_detalle.IdTipoDocumento_id = tipodocumento.id 
        recibo_caja_detalle.IdReciboCaja_id = recibo_caja.id
        recibo_caja_detalle.IdItem_id = iditem
        recibo_caja_detalle.IdPedidoCajaDetalle_id = detalle_pedido.id
        recibo_caja_detalle.valor = item.valor_venta
        recibo_caja_detalle.cantidad = cantidad
        recibo_caja_detalle.pedido_caja = pedido.numero 
        recibo_caja_detalle.valor_total = item.valor_venta*int(float(cantidad))
        recibo_caja_detalle.save()
        recibo_caja_detalle.id += 1
    items = 0    
    for ped in pedido_detalle_regs:
        total = total + ped.valor*ped.cantidad
        items = items + 1
        PedidoCajaDetalle.objects.filter(id=ped.id).update(valor_total=ped.valor*ped.cantidad)
    PedidoCaja.objects.filter(numero=pedido.numero).update(valor_total=total,total_items = items)

    recibo_caja_reg = ReciboCajaDetalle.objects.filter(numero=pedido.recibo_caja)
    total = 0
    items = 0
    for rec in pedido_detalle_regs:
        total = total + rec.valor*rec.cantidad
        PedidoCajaDetalle.objects.filter(id=rec.id).update(valor_total=rec.valor*rec.cantidad)
    ReciboCaja.objects.filter(numero=pedido.recibo_caja).update(valor=total)

def ItemPedidoCaja(request):
    request.session['sel_item']= True
    a = request.session['sel_item']
    iditem = request.GET.get('id', None)
    cantidad = request.GET.get('cantidad', None)
    idpedido = request.session['idpedido']
    #request.session['iditem'] = iditem
    #request.session['cantidad'] = cantidad
    AdicionaItemPedido(iditem,cantidad,idpedido)
    data={'a':0}
    return JsonResponse(data)

def ValidaAdicionaItemPedidoCajaView(request,id):
    idpedido = id
    request.session['idpedido'] = idpedido
    pedido = PedidoCaja.objects.get(id=idpedido)
    if ReciboCaja.objects.filter(numero=pedido.recibo_caja).exists():
        recibo_caja = ReciboCaja.objects.get(numero=pedido.recibo_caja)
        if recibo_caja.pagado == True:
            mensaje1="Tiene un Recibo de Caja asociado:"+recibo_caja.numero+chr(32)
            mensaje2 = ',este recibo esta pago. No se puede modificar.'+chr(32)
            mensaje3 = 'Debe levantar el pago '
            return render(request,'caja/mensaje_error_modificar_detalle_pedido.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'idpedido':pedido.id})
        else:
            mensaje1="Tiene un Recibo de Caja asociado:"+recibo_caja.numero
            mensaje2 = ', éste recibo de caja será modificado'
            mensaje3 = ''
            return render(request,'caja/mensaje_confirma_adiciona_item_pedido_caja.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3})
    else:
        return redirect('adiciona_item_pedido_caja',id=1)


def AdicionaItemPedidoCajaView(request,id):
    idpedido = request.session['idpedido']
    if id == 1:
        return redirect('filtra_item_pedido_caja')
    return redirect('detalle_pedido_caja',idpedido)

def ValidaBorradoPedidoCajaView(request,id):
    request.session['idpedido'] = id
    idpedido = id
    if PedidoCajaDetalle.objects.filter(IdPedidoCaja_id=id).exists():
        mensaje1="No se puede borrar porque tiene Items"
        mensaje2 = '.Debe borrar primero los items correspondientes'
        mensaje3 = ''
        return render(request,'caja/mensaje_error_borrar_pedido.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'idpedido':idpedido})
    else:
        pedido = PedidoCaja.objects.get(id=id)
        if ReciboCaja.objects.filter(pedido_caja=pedido.numero).exists():
            recibo = ReciboCaja.objects.get(IdPedidoCaja_id=id)
            mensaje1="No se puede borrar porque tiene Recibo de Caja"
            mensaje2 = 'Debe anular el recibo de caja No. '+recibo.numero+' '
            mensaje3 = 'para poder borrar el pedido'
            return render(request,'caja/mensaje_error_borrar_pedido.html',{'mensaje1':mensaje1,'idpedido':idpedido})            
        else:
            mensaje1="Esta seguro de borrar este pedido"
            mensaje2 = ''
            mensaje3 = ''
            return render(request,'caja/mensaje_confirma_borra_pedido_caja.html',{'mensaje1':mensaje1,'idpedido':idpedido})

def BuscaPagoView(request):
    idrecibocaja  = request.session['idrecibocaja']
    recibo_caja = ReciboCaja.objects.get(id=idrecibocaja)
    if PagoReciboCaja.objects.filter(recibo_caja=recibo_caja.numero):
        pago = PagoReciboCaja.objects.get(recibo_caja=recibo_caja.numero,estado=1)
        if request.session['recibostodos'] == True:
            nombre_caja = 'Todas'
            pagos_caja = PagosCajaTable(PagoReciboCaja.objects.filter(recibo_caja=recibo_caja.numero,estado=True))
            total_pagos =PagoReciboCaja.objects.filter(recibo_caja=recibo_caja.numero).aggregate(Sum('valor'))['valor__sum']
            context = {'pagos_caja':pagos_caja,'total_pagos': total_pagos,'nombre_caja':nombre_caja}
            return render(request, 'caja/pagos_caja_lista_todos.html', context) 
        else:    
            idcaja = pago.IdCaja
            nombre_caja = idcaja.descripcion
            pagos_caja = PagosCajaTable(PagoReciboCaja.objects.filter(recibo_caja=recibo_caja.numero,estado=True))
            total_pagos =PagoReciboCaja.objects.filter(recibo_caja=recibo_caja.numero).aggregate(Sum('valor'))['valor__sum']
            context = {'pagos_caja':pagos_caja,'total_pagos': total_pagos,'nombre_caja':nombre_caja}
            return render(request, 'caja/pagos_caja_lista.html', context) 
    else:
        mensaje1="Este recibo de caja tiene un pago asociado, "
        mensaje2 = 'que no existe.'
        mensaje3 = 'Borramos el recibo de caja y el pago asociado'
        return render(request,'caja/mensaje_confirma_borra_recibo_caja.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'idrecibocaja':idrecibocaja})            
        
def BuscaReciboCajaView(request,id):
    request.session['idpedido'] = id
    idcaja = request.session['idcaja']
    pedido_caja = PedidoCaja.objects.get(id=id)
    if ReciboCaja.objects.filter(numero=pedido_caja.recibo_caja).exists():
        recibo_caja = ReciboCaja.objects.get(numero=pedido_caja.recibo_caja)
        return redirect('recibo_caja_detalle',recibo_caja.id)
    else:
        if PedidoCajaDetalle.objects.filter(numero=pedido_caja.numero).exists():
            mensaje1="Esta seguro de cerrar este pedido"
            mensaje2 = ''
            mensaje3 = ''
            return render(request,'caja/mensaje_confirma_cierre_pedido_caja.html',{'mensaje1':mensaje1})
        else:
            mensaje1="El pedido no tiene detalle"
            mensaje2 = ''
            mensaje3 = ''
            return render(request,'caja/mensaje_error_cierre_caja_todos.html',{'mensaje1':mensaje1,'idcaja':idcaja})
            
def BorraPedidoCajaView(request,id):
    if id == 1:
        id = request.session['idpedido']
        PedidoCaja.objects.filter(id=id).delete()
    return redirect('direcciona_caja')

class EditaPedidoCajaView(UpdateView):
    model = PedidoCaja
    form_class = PedidoCajaForm
    template_name = 'caja/pedido_caja_form.html'

    def get_success_url(self, *args, **kwargs):
        #self.request.session['vaya_a_lista_pedidos']= True
        idpedidocaja = self.object.pk
        pedido_caja = PedidoCaja.objects.get(id=idpedidocaja)
        idcaja = pedido_caja.IdCaja_id
        return reverse_lazy('direcciona_pedido')

def DireccionaPedidoDetalleView(request):
    ## Para la salida de la seleccion de items 
    #idpedido = request.session['idpedidocaja']
    if request.session['pedidostodos'] == True:
        return redirect('pedido_caja_lista_todos')
    else: 
        #idcaja = request.session['idcaja']
        idpedido = request.session['idpedidocaja']
        return redirect('detalle_pedido_caja',idpedido) 

def DireccionaReciboCajaDetalleView(request):
    ## Para la salida de la seleccion de items 
    #idpedido = request.session['idpedidocaja']
    #print('recibos Todos',request.session['recibostodos'])
    if request.session['recibostodos']== True and request.session['pedidostodos'] == True:
        return redirect('recibo_caja_lista_todos')
    else: 
        return redirect('recibo_caja_lista') 

def DireccionaPagoCajaDetalleView(request):
    ## Para la salida de la seleccion de items 
    #idpedido = request.session['idpedidocaja']
    if request.session['pagostodos'] == True:
        return redirect('pago_caja_lista_todos')
    else: 
        return redirect('pagos_caja_lista') 

def DireccionaPagoCaja(request):
    idcaja = request.session['idcaja']
    return redirect('pagos_caja_lista')   

def DireccionaPedidoView(request):
    if request.session['pedidostodos'] == True:
        return redirect('pedido_caja_lista_todos')
    else:
        if request.session['pedidosconsolidados'] == True:
            #idhabitacion = request.session['idhabitacion']
            idhabitacion = request.session['id_habitacion_consolidar']
            return redirect('pedidos_caja_consolidados',idhabitacion)
        else:       
            return redirect('pedido_caja_lista') 

def DireccionaReciboCajaView(request):
    return redirect('recibo_caja_lista')

def ReciboCajaListaView(request):
    request.session['recibostodos'] = False
    lista_id = []
    request.session['lista_id_filtro_recibo_caja'] = lista_id
    idcaja = request.session['idcaja']
    caja = Caja.objects.get(id=idcaja)
    if request.session['pedidosconsolidados'] == True:
        idhabitacion = request.session['id_habitacion_consolidar']
        queryset = ReciboCaja.objects.filter(IdHabitacion_id=idhabitacion).order_by('numero').reverse()
        total_recibos =ReciboCaja.objects.filter(IdHabitacion_id=idhabitacion).aggregate(Sum('valor'))['valor__sum']
    else:   
        queryset = ReciboCaja.objects.filter(IdCaja_id=idcaja).order_by('numero').reverse()
        total_recibos =ReciboCaja.objects.filter(IdCaja_id=idcaja).aggregate(Sum('valor'))['valor__sum']
    f = RecibosCajaFilter(request.GET, queryset=queryset)
    recibos_caja = RecibosCajaTable(f.qs)
    for n in f.qs:
        lista_id.append(n.id)
    #total_recibos =ReciboCaja.objects.filter(IdCaja_id=idcaja).aggregate(Sum('valor'))['valor__sum']
    recibos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
    request.session['lista_id_filtro_recibo_caja']  = lista_id
    context = {'recibos_caja':recibos_caja,'filter':f,'nombre_caja':caja.descripcion,'total_recibos':total_recibos}
    return render(request, 'caja/recibos_caja_lista.html', context)
    

def ReciboCajaDetalleListaView(request,id):
    idrecibocaja = id
    recibo_caja = ReciboCaja.objects.get(id=idrecibocaja)
    caja = Caja.objects.get(id=recibo_caja.IdCaja_id)
    recibo_caja_table = RecibosCajaTable(ReciboCaja.objects.filter(id=idrecibocaja))
    recibo_detalle_caja = RecibosCajaDetalleTable(ReciboCajaDetalle.objects.filter(IdReciboCaja_id=idrecibocaja))
    total_recibos =ReciboCajaDetalle.objects.filter(IdReciboCaja_id=idrecibocaja).aggregate(Sum('valor_total'))['valor_total__sum']
    context = {'recibo_detalle_caja':recibo_detalle_caja,'recibo_caja':recibo_caja_table,'idrecibo':idrecibocaja,'nombre_caja':caja.descripcion,'valor':recibo_caja.valor,'total':total_recibos}
    return render(request, 'caja/recibos_caja_detalle.html', context) 

def ReciboCajaListaTodosView(request):
    lista_id = []
    request.session['lista_id_filtro_recibo_caja'] = lista_id
    request.session['recibostodos'] = True
    queryset = ReciboCaja.objects.all().order_by('numero').reverse()
    f = RecibosCajaFilter(request.GET, queryset=queryset)
    recibos_caja = RecibosCajaTable(f.qs)
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
        request.session['lista_id_filtro_recibo_caja']  = lista_id
    total_recibos =ReciboCaja.objects.filter(id__in=lista_id).aggregate(Sum('valor'))['valor__sum']
    recibos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
    nombre_caja = 'Todas'
    context = {'recibos_caja':recibos_caja,'filter':f,'nombre_caja':nombre_caja,'total_recibos':total_recibos}
    request.session['recibostodos']= True
    return render(request, 'caja/recibos_caja_lista_todos.html', context)

class CreaTerceroCierrePedidoCajaView(LoginRequiredMixin,CreateView):
    model = Tercero
    template_name = 'caja/tercero_recibo_caja_form.html'
    form_class = TerceroReciboCajaForm
    
    def get_success_url(self):
        idtercero = self.object.id
        #idtercero = Tercero.objects.latest('id')
        tercero = Tercero.objects.get(id=idtercero.id)
        self.request.session['idtercero' ] = tercero.id
        return redirect('crea_recibo_caja')   

    def get_initial(self,*args,**kwargs):
        id =self.kwargs['id']
        self.request.session['tipo_pago'] = id
        initial=super(CreaTerceroCierrePedidoCajaView,self).get_initial(**kwargs)
        valor_defecto_pais = ValorDefecto.objects.get(idValor='02')
        pais = Pais.objects.get(idPais=valor_defecto_pais.valor)
        initial['IdPais'] = pais.id
        #initial['IdTipoTercero'] = 1
        return initial
    
    def form_valid(self, form):
        id =self.kwargs['id']
        if form.is_valid():
            tercero = form.save(commit=False)
            registros = RegistroHotel.objects.count()
            sregistro= str(registros+1)
            idtercero = sregistro.zfill(8)
            tercero = form.save(commit=False)
            tercero.idTercero = idtercero
            tercero.IdUsuario_id = self.request.user.id
            #tercero.apenom = self.apel1.strip()+" "+self.apel2.strip()+" "+self.nombre1.strip()+" "+self.nombre2.strip()
            tercero.save()
            #idtercero = Tercero.objects.latest('id')
            #tercero = Tercero.objects.get(id=idtercero.id)
            self.request.session['idtercero'] = tercero.id
            print('Tercero Id: ',tercero.id)
            Tercero.objects.filter(id=tercero.id).update(apenom = tercero.apel1.strip()+" "+tercero.apel2.strip()+" "+tercero.nombre1.strip()+" "+tercero.nombre2.strip())
            #return redirect('cierre_pedido_caja')
            if id == 1:
                return redirect('crea_recibo_caja')   
            elif id == 2:
                return redirect('selecciona_caja_recibo_caja_consolidado')
        
class BuscaTerceroCierrePedidoCajaView(SingleTableMixin, FilterView):
    table_class = TercerosListaTable
    model = Tercero
    template_name = "core/terceros_caja_filter.html"
    filterset_class = TerceroNombreFilter
    paginate_by = 8

def GuardaIdPedidoCajaView(request):
    idPedido = request.GET.get('id', None)
    request.session['idpedidocaja'] = idPedido
    data = {'id':idPedido}
    return JsonResponse(data) 

def GuardaIdHabitacionView(request):
    idHabitacion = request.GET.get('id', None)
    request.session['idhabitacion'] = idHabitacion
    data = {'id':idHabitacion}
    return JsonResponse(data) 

def SeleccionaTerceroPedidoCaja(request):
    idTercero = request.GET.get('id', None)
    request.session['idtercero'] = idTercero
    data = {'id':idTercero}
    return JsonResponse(data) 

def GuardaIdPedidoCaja(request):
    idPedido = request.GET.get('id', None)
    request.session['idpedidocaja'] = idPedido
    data = {'id':idPedido}
    return JsonResponse(data) 

def CierrePedidoCajaView(request):
    return redirect('busca_tercero_cierre_pedido_caja')

""" def ConfirmaCierrePedidoCajaView(request,id):
            if PedidoCaja.objects.filter(id=id,cerrado=True).exists():
            mensaje1="No se puede cerrar porque ya esta cerrado,"
            mensaje2 = ''
            mensaje3 = ''
            return render(request,'caja/mensaje_error_cierre_caja.html',{'mensaje1':mensaje1})
        else:
            mensaje1="Esta seguro de cerrar este pedido"
            mensaje2 = ''
            mensaje3 = ''
            return render(request,'caja/mensaje_confirma_cierre_pedido_caja.html',{'mensaje1':mensaje1}) """

def ValidaCierrePedidoCajaView(request,id):
    if id == 1:
       return redirect('cierre_pedido_caja')     
    else:
        #request.session['retorne_pedido_caja'] = True    
        return redirect('pedido_caja_lista')    
    
def CreaReciboCajaView(request):
    request.session['recibostodos'] = False
    request.session['consolidar'] = False
    idTercero = request.session['idtercero'] 
    id = request.session['idpedidocaja']
    idCaja = request.session['idcaja']
    pedido_caja = PedidoCaja.objects.get(id=id)
    sucursal_defecto = ValorDefecto.objects.get(idValor='01')
    sucursal =Sucursal.objects.get(idSucursal=sucursal_defecto.valor)
    recibo_caja = ReciboCaja()
    tipodocumento = TipoDocumentoCaja.objects.get(idTipo='02')
    anumero = tipodocumento.actual +1
    snumero = str(anumero).zfill(tipodocumento.longitud)
    snumero = tipodocumento.caracteres+snumero
    recibo_caja.IdTipoDocumento_id = tipodocumento.id 
    recibo_caja.numero =  snumero
    recibo_caja.fecha = date.today()
    recibo_caja.estado = True
    recibo_caja.pedido_caja = pedido_caja.numero
    recibo_caja.IdTercero_id = idTercero
    recibo_caja.IdMesa_id = pedido_caja.IdMesa_id
    recibo_caja.IdHabitacion_id = pedido_caja.IdHabitacion_id
    recibo_caja.IdCaja_id = idCaja
    recibo_caja.IdSucursal_id = sucursal_defecto.id
    recibo_caja.IdUsuario_id = request.user.id
    recibo_caja.valor = pedido_caja.valor_total
    recibo_caja.save()
    CreaDocumentoSalidaInventariosCabeza(date.today(),snumero,sucursal_defecto.id,request.user.id)
    PedidoCaja.objects.filter(id=id).update(cerrado=True)
    ####Mesa.objects.filter(id=pedido_caja.IdMesa_id).update(en_uso=False)
    TipoDocumentoCaja.objects.filter(idTipo='02').update(actual = anumero ) 

    recibo_caja = ReciboCaja.objects.get(numero=snumero)
    recibo_caja_detalle = ReciboCajaDetalle()
    pedido_caja_detalle = PedidoCajaDetalle.objects.filter(numero=pedido_caja.numero)
    for ped in pedido_caja_detalle:
        recibo_caja_detalle.numero = snumero
        recibo_caja_detalle.IdTipoDocumento_id = tipodocumento.id 
        recibo_caja_detalle.IdReciboCaja_id = recibo_caja.id
        recibo_caja_detalle.IdItem_id = ped.IdItem_id
        recibo_caja_detalle.IdPedidoCajaDetalle_id = ped.id
        recibo_caja_detalle.valor = ped.valor
        recibo_caja_detalle.cantidad = ped.cantidad
        recibo_caja_detalle.valor_total = ped.valor_total
        recibo_caja_detalle.save()
        recibo_caja_detalle.id += 1
    pedido_caja = PedidoCaja.objects.filter(id=id).update(recibo_caja=snumero)    
    return redirect('recibo_caja_detalle',recibo_caja.id) 

def ValidaEditaItemPedidoCajaView(request,id):
    detalle_pedido = PedidoCajaDetalle.objects.get(id=id)
    #recibo_caja_detalle = ReciboCajaDetalle.objects.get(IdPedidoCajaDetalle=id)
    #recibo_caja = ReciboCaja.objects.get(id=recibo_caja_detalle.IdReciboCaja_id) 
    idpedido = detalle_pedido.IdPedidoCaja_id
    pedido = PedidoCaja.objects.get(id=idpedido)
    request.session['id_det_pedido'] = id
    #request.session['id_det_recibo_caja_detalle'] = recibo_caja_detalle.id
    if ReciboCaja.objects.filter(numero=pedido.recibo_caja).exists():
        recibo_caja=ReciboCaja.objects.get(numero=pedido.recibo_caja)
        if recibo_caja.pagado == True:
            mensaje1="Tiene un Recibo de Caja Asociado:"+pedido.recibo_caja+chr(32)
            mensaje2 = ',este recibo esta pago. No se puede modificar.'+chr(32)
            mensaje3 = 'Debe levantar el pago '
            return render(request,'caja/mensaje_error_modificar_detalle_pedido.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'idpedido':pedido.id})
        else:
            mensaje1="Tiene un Recibo de Caja Asociado:"+pedido.recibo_caja+chr(32)
            mensaje2 = '.Este recibo será modificado'+chr(32)
            mensaje3 = ''
            #return render(request,'caja/mensaje_error_modificar_detalle_pedido.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'idpedido':pedido.id})
            return render(request,'caja/mensaje_confirma_edita_detalle_pedido_caja.html',{'mensaje1':mensaje1,'mensaje2':mensaje2})
    else:
        mensaje1="Esta seguro de editar este item del pedido?"
        mensaje2 = ''
        mensaje3 = ''
        return render(request,'caja/mensaje_confirma_edita_detalle_pedido_caja.html',{'mensaje1':mensaje1})

def EditaDetallePedidoCajaView(request,id):
    iddetalle = request.session['id_det_pedido']
    detalle_pedido = PedidoCajaDetalle.objects.get(id=iddetalle)
    pedido_caja = PedidoCaja.objects.get(id=detalle_pedido.IdPedidoCaja_id)
    if id == 1:
        year = pedido_caja.fecha
        anio = year.year
        mes = year.month
        instancia = PedidoCajaDetalle.objects.get(id=iddetalle)
        form = PedidoCajaDetalleForm(request.POST or None, instance = instancia)
        salida = Salida.objects.get(pedido_caja=pedido_caja.numero)
        bodega_defecto = ValorDefecto.objects.get(idValor='05')
        bodega = Bodega.objects.get(idBodega=bodega_defecto.valor)
        item = MaestroItem.objects.get(id=detalle_pedido.IdItem_id)
        if form.is_valid():
            mes = year.month
            InventariosView.ReversaAcumuladosSalidaInventarios(detalle_pedido.IdItem_id,detalle_pedido.cantidad,mes,anio)
            #ReversaAcumuladosInventarios(detalle_pedido.IdItem_id,detalle_pedido.cantidad,mes,anio)
            instancia = form.save(commit=False)
            SalidaDetalle.objects.filter(pedido_detalle_id=iddetalle).update(IdItem=instancia.IdItem,cantidad=instancia.cantidad,valor=instancia.valor,valor_total=instancia.cantidad*instancia.valor)
            invinic=False
            InventariosView.ActualizaAcumuladosInventarios(instancia.IdItem_id,instancia.cantidad,0,mes,anio,'salida',0,invinic)
            #ActualizaAcumuladosInventarios(detalle_pedido.IdItem_id,instancia.cantidad,mes,anio,'salida',bodega.id)
            instancia.save()
            PedidoCajaDetalle.objects.filter(id=iddetalle).update(valor_total=instancia.cantidad*instancia.valor)
            ReciboCajaDetalle.objects.filter(IdPedidoCajaDetalle=iddetalle).update(IdItem_id=instancia.IdItem,cantidad=instancia.cantidad,valor_total=instancia.cantidad*instancia.valor)
            pedido_caja_detalle = PedidoCajaDetalle.objects.filter(numero=pedido_caja.numero)
            total = 0
            i = 0
            for n in pedido_caja_detalle:
                total = total + n.cantidad*n.valor
                i += 1
            PedidoCaja.objects.filter(id=detalle_pedido.IdPedidoCaja_id).update(valor_total=total,total_items=i)    
            return redirect('detalle_pedido_caja',pedido_caja.id)
        else:
            form = PedidoCajaDetalleForm(instance=instancia)
        return render(request, 'caja/pedido_caja_detalle_form.html', {'form':form})
    else:
        return redirect('detalle_pedido_caja',pedido_caja.id )
       
def ValidaBorradoDetallePedidoCajaView(request,id):
    request.session['idpedidocaja'] = id
    mensaje1="Esta seguro de borrar este registro"
    mensaje2 = ''
    mensaje3 = ''
    return render(request,'caja/mensaje_confirma_borra_pedido_caja.html',{'mensaje1':mensaje1})

def ValidaBorradoItemPedidoCajaView(request,id):
    detalle_pedido = PedidoCajaDetalle.objects.get(id=id)
    idpedido = detalle_pedido.IdPedidoCaja_id
    pedido = PedidoCaja.objects.get(id=idpedido)
    request.session['id_det_pedido'] = id
    # Esto por que hay varios pedidos en un recibo
    if ReciboCajaDetalle.objects.filter(pedido_caja=pedido.numero):
        recibo_caja = ReciboCaja.objects.get(numero=pedido.recibo_caja)
        if recibo_caja.pagado:
            mensaje1="Tiene un Recibo de Caja Asociado:"+pedido.recibo_caja+chr(32)
            mensaje2 = ',este recibo esta pago. No se puede modificar'+chr(32)
            mensaje3 = 'el pedido, debe levantar el pago '
            return render(request,'caja/mensaje_error_borrar_detalle_pedido.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'idpedido':pedido.id})
        else:
            mensaje1="Tiene un Recibo de Caja Asociado:"+pedido.recibo_caja+chr(32)
            mensaje2 = ',este recibo será modificado '
            mensaje3 = ' '
            return render(request,'caja/mensaje_confirma_borra_item_pedido_caja.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3})
    else:
        mensaje1="Esta seguro de borrar este item del pedido"
        mensaje2 = ''
        mensaje3 = ''
        return render(request,'caja/mensaje_confirma_borra_item_pedido_caja.html',{'mensaje1':mensaje1})

def BorraFormulaProducto(numero_ped,iditem,cantidad):
    if Receta.objects.filter(producto_id=iditem).exists():
        receta = Receta.objects.get(producto_id=iditem)
        pedido = PedidoCaja.objects.get(numero=numero_ped)
        salida = Salida.objects.get(pedido_caja=pedido.numero)
        year = pedido.fecha
        anio = year.year
        mes = year.month
        ingredientes_receta = RecetaIngrediente.objects.filter(receta_id=receta.id)
        for i in ingredientes_receta:
            ingrediente = Ingrediente.objects.get(id=i.ingrediente_id)
            item = MaestroItem.objects.get(id=ingrediente.ingrediente_id)
            cantidad_def = cantidad * i.cantidad_necesaria
            InventariosView.ReversaAcumuladosSalidaInventarios(item.id,cantidad_def,mes,anio)
            invinic = 0
            InventariosView.ActualizaAcumuladosInventarios(item.id,0,0,mes,anio,'salida',0,invinic)
            SalidaDetalle.objects.filter(numero=salida.numero,IdItem_id=item.id).delete()  
    return

def BorraItemPedidoCajaView(request,id):
    id_det_pedido = request.session['id_det_pedido']
    detalle_pedido = PedidoCajaDetalle.objects.get(id=id_det_pedido)
    pedido_caja = PedidoCaja.objects.get(numero=detalle_pedido.numero)
    year = pedido_caja.fecha
    anio = year.year
    mes = year.month
    item = MaestroItem.objects.get(id=detalle_pedido.IdItem_id)
    if id == 1:
        BorraFormulaProducto(pedido_caja.numero,detalle_pedido.IdItem,detalle_pedido.cantidad)
        InventariosView.ReversaAcumuladosSalidaInventarios(detalle_pedido.IdItem_id,detalle_pedido.cantidad,mes,anio)
        PedidoCajaDetalle.objects.filter(numero=pedido_caja.numero,IdItem_id=detalle_pedido.IdItem_id).delete()
        SalidaDetalle.objects.filter(pedido_detalle_id=id_det_pedido).delete()
        invinic = 0
        InventariosView.ActualizaAcumuladosInventarios(detalle_pedido.IdItem_id,0,0,mes,anio,'salida',0,invinic)
        i = 0
        total=0
        detalle = PedidoCajaDetalle.objects.filter(numero=detalle_pedido.numero)
        for n in detalle:
            total = total + n.cantidad*n.valor
            i += 1
        PedidoCaja.objects.filter(id=detalle_pedido.IdPedidoCaja_id).update(valor_total=total,total_items=i)    
    return redirect('detalle_pedido_caja',pedido_caja.id)
           
    
def BorraPedidoCajaView(request,id):
    idpedido = request.session['idpedidocaja']
    idcaja = request.session['idcaja']
    if id == 1:
        aa = Caja.objects.filter(id=id).exists()
        if aa != True:
            caja = Caja.objects.get(idCaja='99')
            idcaja = caja.id
        PedidoCaja.objects.filter(id=idpedido).delete()
    return redirect('ingreso_caja')


class PagoReciboCajaView(LoginRequiredMixin,CreateView):
    model = PagoReciboCaja
    template_name = 'caja/pago_caja_form.html'
    form_class = PagoReciboCajaForm
    
    def get_initial(self,*args,**kwargs):
        id =self.kwargs['id']
        recibo_caja = ReciboCaja.objects.get(id=id)
        initial=super(PagoReciboCajaView,self).get_initial(**kwargs)
        initial['recibo_caja'] = recibo_caja.numero
        initial['valor'] = recibo_caja.valor
        initial['IdTipoPago'] = 2  
        return initial
    
    def get_success_url(self):
        return reverse_lazy('recibo_caja_detalle',self.kwargs['id'])   

    def form_valid(self, form):
        if form.is_valid():
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
            idrecibocaja =self.kwargs['id']
            recibo_caja = ReciboCaja.objects.get(id=idrecibocaja)
            idcaja = recibo_caja.IdCaja_id
                        
            pago_caja.fecha = timezone.now()
            pago_caja.numero = snumero   
            pago_caja.IdTercero_id = recibo_caja.IdTercero_id
            pago_caja.IdTipoDocumento_id = tipodocumento.id
            pago_caja.IdSucursal_id = sucursal_defecto.id
            pago_caja.IdUsuario_id = self.request.user.id
            pago_caja.IdCaja_id = idcaja 
            pago_caja.recibo_caja = recibo_caja.numero
            pago_caja.estado = 1
            pago_caja.save()
            pago_caja.id += 1
            print('Recibo Caja:',id)
            ReciboCaja.objects.filter(id=idrecibocaja).update(pagado=True)
            TipoDocumentoCaja.objects.filter(idTipo='04').update(actual = anumero ) 
            if self.request.session['recibostodos'] == True:
                return redirect('pagos_caja_lista_todos')
            else:
                if self.request.session['consolidar'] == True:
                   return redirect('pagos_caja_lista_consolidado')
                else:
                   return redirect('pagos_caja_lista')

def GuardaIdReciboCaja(request):
    idrecibocaja = request.GET.get('id', None)
    request.session['idrecibocaja'] = idrecibocaja
    data = {'id':idrecibocaja}
    return JsonResponse(data) 

def MensajeReciboCajaPagadoView(request):
    id = request.session['idrecibocaja']
    recibo_caja = ReciboCaja.objects.get(id=id) 
    mensaje1 = "El recibo de Caja No."+recibo_caja.numero
    mensaje2 = " ,ya está pago "
    pago = PagoReciboCaja.objects.get(recibo_caja=recibo_caja.numero)
    mensaje3 = " Pago No. : "+pago.numero+' de '+str(pago.fecha)   
    context={'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3}
    return render(request, 'caja/mensaje_recibo_caja_pagado.html', context) 

""" import pandas as pd
from django.http import JsonResponse

def agrupar_registros_por_campo(request):
    # Suponiendo que el archivo está en 'Informacion/Archivo.csv'
    archivo = 'Informacion/Archivo.csv'
    df = pd.read_csv(archivo)
    # Cambia 'campo' por el nombre real del campo por el que quieres agrupar
    agrupado = df.groupby('campo').size().reset_index(name='cantidad')
    # Convertir a lista de diccionarios para respuesta JSON
    resultado = agrupado.to_dict(orient='records')
    return JsonResponse({'resultado': resultado}) """

from django.db.models import Count
#from django.http import JsonResponse
#from .models import PagoReciboCaja
from django.template import loader

def CuadreCajaView(request,id):
    caja = Caja.objects.get(id=id)
    if request.method == 'GET':
        query= request.GET.get('q')
        fecha=query
        submitbutton= request.GET.get('submit')
        request.session['fecha_cuadre_caja'] = fecha
        # Agrupa por IdTipoPago y cuenta la cantidad de pagos por cada tipo
        pago_caja = PagoReciboCaja.objects.filter(fecha=fecha,IdCaja_id=id).values('IdTipoPago','IdTipoPago__descripcion').annotate(total_valor=Sum('valor')).order_by('IdTipoPago__descripcion')
        total_caja = 0
        for i in pago_caja:
            total_caja = total_caja + i['total_valor']   
        context = {
        'pago_caja': pago_caja,'idcaja':id,'nombre_caja':caja.descripcion,'total_caja':total_caja,
        }
        return render(request, 'caja/cuadre_caja.html', context)     
    else:
        # Agrupa por IdTipoPago y cuenta la cantidad de pagos por cada tipo
        pago_caja = PagoReciboCaja.objects.filter(fecha=fecha,IdCaja_id=id).values('IdTipoPago','IdTipoPago__descripcion').annotate(total_valor=sum('valor')).order_by('IdTipoPago__descripcion')
        context = {
        'pago_caja': pago_caja,'idcaja':id,'nombre_caja':caja.descripcion,'total_caja':total_caja,
        }
        print(context)
        return render(request, 'caja/cuadre_caja2.html', context) 
 
 
def PagosCajaListaView(request):
    request.session['pagostodos'] = False
    lista_id = []
    idcaja = request.session['idcaja']
    caja = Caja.objects.get(id=idcaja)
    request.session['lista_id_filtro_pago_caja'] = lista_id
    queryset = PagoReciboCaja.objects.filter(IdCaja_id=idcaja).order_by('numero').reverse()
    f = PagosCajaFilter(request.GET, queryset=queryset)
    pagos_caja = PagosCajaTable(f.qs)
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
    request.session['lista_id_filtro_pago_caja'] = lista_id  
    total_pagos =PagoReciboCaja.objects.filter(id__in=lista_id).aggregate(Sum('valor'))['valor__sum']  
    pagos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
    context = {'pagos_caja':pagos_caja,'filter':f,'nombre_caja':caja.descripcion,'total_pagos': total_pagos}
    return render(request, 'caja/pagos_caja_lista.html', context) 
    
def PagosCajaListaConsolidadoView(request):
    request.session['pagostodos'] = False
    idrecibocaja = request.session['idrecibocaja']
    lista_id = []
    recibo = ReciboCaja.objects.get(id=idrecibocaja)
    caja = Caja.objects.get(id=recibo.IdCaja_id)
    request.session['lista_id_filtro_pago_caja'] = lista_id
    queryset = PagoReciboCaja.objects.filter(recibo_caja=recibo.numero).order_by('numero').reverse()
    f = PagosCajaFilter(request.GET, queryset=queryset)
    pagos_caja = PagosCajaTable(f.qs)
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
    request.session['lista_id_filtro_pago_caja'] = lista_id  
    total_pagos =PagoReciboCaja.objects.filter(recibo_caja=recibo.numero).aggregate(Sum('valor'))['valor__sum']  
    pagos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
    context = {'pagos_caja':pagos_caja,'filter':f,'nombre_caja':caja.descripcion,'total_pagos': total_pagos}
    return render(request, 'caja/pagos_caja_lista.html', context)     
    
def PagosCajaListaTodosView(request):
    request.session['pagostodos'] = True
    lista_id = []
    request.session['lista_id_filtro_pago_caja'] = lista_id
    queryset = PagoReciboCaja.objects.all().order_by('numero').reverse()
    f = PagosCajaFilter(request.GET, queryset=queryset)
    pagos_caja = PagosCajaTable(f.qs)
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
        request.session['lista_id_filtro_pago_caja'] = lista_id  
    total_pagos =PagoReciboCaja.objects.filter(id__in=lista_id).aggregate(Sum('valor'))['valor__sum']  
    pagos_caja.paginate(page=request.GET.get("page", 1), per_page=8)
    nombre_caja = 'Todas'
    context = {'pagos_caja':pagos_caja,'filter':f,'nombre_caja':nombre_caja,'total_pagos': total_pagos}
    return render(request, 'caja/pagos_caja_lista_todos.html', context) 

def ValidaBorradoPagoReciboCajaView(request,id):
    request.session['idpago'] = id
    mensaje1="Esta seguro de borrar este pago?"
    mensaje2 = ''
    mensaje3 = ''
    return render(request,'caja/mensaje_confirma_borra_pago_caja.html',{'mensaje1':mensaje1})

def BorraPagoReciboCajaView(request,id):
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
    idcaja = request.session['idcaja']
    if request.session['pagostodos'] == True:
        return redirect('pagos_caja_lista_todos')
    else:
        if request.session['pedidosconsolidados'] == True:
            return redirect('pagos_caja_lista_consolidado')
        else:       
            return redirect('pagos_caja_lista')

def CreaDocumentosInventariosPedidosCajaView(request):
    año_defecto = ValorDefecto.objects.get(idValor='06')
    anio = str(año_defecto.valor)
    bodegas = Bodega.objects.all()
    for bod in bodegas:
        PoneCerosAcumuladosInventarios(anio,bod.id)
    CreaDocumentosInventariosPedidosCaja()
    return redirect('home')

def CreaDocumentosInventariosPedidosCaja():    
    # Borra los documentos de salida por pedido de inventarios
    salida = Salida.objects.get(idTipo='04')
    Salida.objects.filter(IdTipoDocumento_id=salida.id).delete()
    SalidaDetalle.objects.filter(IdTipoDocumento_id=salida.id).delete()
    TipoDocumentoInv.objects.filter(idTipo='04').update(actual=0)
    pedidos = PedidoCaja.objects.all()
    #bodega_defecto = ValorDefecto.objects.get(idValor='05')
    #bodega =Bodega.objects.get(idBodega=bodega_defecto.valor)
    for k in pedidos:
        idsucursal = k.IdSucursal_id
        idusuario = k.IdUsuario_id
        CreaDocumentoSalidaInventariosCabeza(k.fecha,k.numero,idsucursal,idusuario)
        pedido_detalle = PedidoCajaDetalle.objects.filter(numero=k.numero)
        for m in pedido_detalle:
            num_ped = m.numero
            iditem = m.IdItem_id
            maestro_inv = MaestroItem.objects.get(id=m.IdItem_id)
            if maestro_inv.acumula == True:
                CreaDocumentoSalidaInventariosCuerpo(num_ped,iditem,m.cantidad,m.valor_total,m.valor_total*int(float(m.cantidad)))
        
def ValidaBorradoReciboCajaView(request,id):
    request.session['idrecibocaja'] = id
    idrecibocaja = id
    if ReciboCaja.objects.filter(id=idrecibocaja,pagado=True):
        recibo_caja = ReciboCaja.objects.get(id=idrecibocaja)
        idcaja = recibo_caja.IdCaja_id
        if PagoReciboCaja.objects.filter(recibo_caja=recibo_caja.numero).exists():
            pago = PagoReciboCaja.objects.get(recibo_caja=recibo_caja.numero)
            mensaje1="No se puede borrar porque tiene Pago,"
            mensaje2 = 'Debe anular el pago No. '+pago.numero+' '
            mensaje3 = 'para poder borrar el recibo de caja'
            return render(request,'caja/mensaje_error_borrar_recibo_caja.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'idrecibocaja':idrecibocaja})            
        else:
            mensaje1="Tiene un pago asociado que no existe "
            mensaje2 = 'Desea borrar este recibo de caja?'
            mensaje3 = ''
            return render(request,'caja/mensaje_confirma_borra_recibo_caja.html',{'mensaje1':mensaje1,'mensaje2':mensaje2,'mensaje3':mensaje3,'idrecibocaja':idrecibocaja})            

    else:
        mensaje1="Esta seguro de borrar este recibo de caja?"
        mensaje2 = ''
        mensaje3 = ''
        return render(request,'caja/mensaje_confirma_borra_recibo_caja.html',{'mensaje1':mensaje1,'idrecibocaja':idrecibocaja})

def BorraReciboCajaView(request,id):
    idrecibocaja = request.session['idrecibocaja']
    idcaja = request.session['idcaja']
    if id == 1:
        recibo_caja = ReciboCaja.objects.get(id=idrecibocaja)
        PedidoCaja.objects.filter(recibo_caja=recibo_caja.numero).update(recibo_caja='',cerrado=False)
        valor_defecto = ValorDefecto.objects.get(idValor='08')
        if valor_defecto.valor == 1:
            ReciboCajaDetalle.objects.filter(numero=recibo_caja.numero).delete()
            ReciboCaja.objects.filter(id=idrecibocaja).delete()
        else:
            ReciboCaja.objects.filter(id=idrecibocaja).update(detalle='Recibo Anulado',valor=0,pedido_caja='',pagado=0,IdMesa_id=1,IdHabitacion_id=1)
            ReciboCajaDetalle.objects.filter(numero=recibo_caja.numero).delete()
    return redirect('direcciona_recibo_caja')

import pyodbc 

def ImpresionRecibosCajaPdfView(request):
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
    pdf.drawString(110, y, u""+empresa.nombre)
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(100, y, u"RECIBO DE CAJA")
    pdf.setFont("Helvetica", 9)
    lista_id_recibos= request.session['lista_id_filtro_recibo_caja']
    if request.session['lista_id_filtro_recibo_caja']:
        id_recibos = request.session['lista_id_filtro_recibo_caja']
        recibos = ReciboCaja.objects.filter(id__in=id_recibos)
    else:
        recibos = ReciboCaja.objects.all()    
    y -= 5    
    for i in recibos:
        pdf.setFont("Helvetica", 9) 
        cuerpo = ReciboCajaDetalle.objects.filter(numero=i.numero)
        pdf.line(30,y,330,y)
        y -= 15
        pdf.drawString(30,y , u"Número : "+str(i.numero))
        pdf.drawString(180,y , u"Fecha : "+i.created.strftime("%Y-%m-%d %H:%M:%S"))
        y -= 5
        pdf.line(30,y,330,y)
        y -= 15
        pdf.drawString(30, y, u"Cliente : "+str(i.IdTercero))
        y -= 15
        pdf.drawString(30, y, u"Pedido Caja : "+str(i.pedido_caja))
        y -= 15
        pdf.drawString(30, y, u"Habitación   : "+str(i.IdHabitacion))
        y -= 15
        pdf.drawString(30, y, u"Mesa : "+str(i.IdMesa))
        y -= 15
        detalle = P(i.detalle)
        detalle = str(i.detalle).strip()
        pdf.drawString(30, y, u"Detalle : "+detalle)
        y -= 20

        cuerpo = ReciboCajaDetalle.objects.filter(numero=i.numero)
        registros = ReciboCajaDetalle.objects.filter(numero=i.numero).count()
        total_recibo = cuerpo.aggregate(Sum('valor_total'))['valor_total__sum']
        total = total_recibo
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Producto', 'Cantidad', 'Valor Unit.', 'Valor Total')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(cuerpo.IdItem.descripcion[0:40], cuerpo.cantidad, '{:,}'.format(cuerpo.valor), '{:,}'.format(cuerpo.valor_total)) for cuerpo in cuerpo]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_recibo = Table([encabezados] + detalles, colWidths=[5 * cm, 1.1 * cm, 2.1 * cm, 2.3 * cm])
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
        y = y -(registros*25)
        if y<=40:
           pdf.showPage()
           y= 750 
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_recibo.wrapOn(pdf, 300, 800)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_recibo.drawOn(pdf, 30,y)
        y -= 10
        if total_recibo:
            pdf.setFont("Helvetica", 9)
            pdf.drawString(200, y, u"Total Recibo      : "+('{:,}'.format(total_recibo)+'.00'))
            y -= 20
       
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionReciboCajaUnoView(request,id):
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
    pdf.drawString(110, y, u""+empresa.nombre)
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(100, y, u"RECIBO DE CAJA")
    pdf.setFont("Helvetica", 9)
    recibo = ReciboCaja.objects.filter(id=id)
    for i in recibo:
        pdf.setFont("Helvetica", 9) 
        cuerpo = ReciboCajaDetalle.objects.filter(numero=i.numero)
        x = 330
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
        pdf.drawString(30, y, u"Mesa : "+str(i.IdMesa))
        pdf.drawString(150, y, u"Habitación   : "+str(i.IdHabitacion))
        y -= factor
        y -= 10
        #y = 760
        cuerpo = ReciboCajaDetalle.objects.filter(numero=i.numero)
        total_recibo = cuerpo.aggregate(Sum('valor_total'))['valor_total__sum']
        total = total_recibo
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Producto', 'Cantidad', 'Valor Unit.', 'Valor Total')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(cuerpo.IdItem.descripcion[0:40], cuerpo.cantidad, '{:,}'.format(cuerpo.valor), '{:,}'.format(cuerpo.valor_total)) for cuerpo in cuerpo]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_recibo = Table([encabezados] + detalles, colWidths=[5 * cm, 1.1 * cm, 2.1 * cm, 2.3 * cm])
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
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_recibo.wrapOn(pdf, 300, 800)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_recibo.drawOn(pdf, 30,y)
        y -= 10
        if total_recibo:
            pdf.setFont("Helvetica", 9)
            pdf.drawString(200, y, u"Total Recibo      : "+('{:,}'.format(total_recibo)+'.00'))
        y -= 20
        
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionRecibosCajaTodosPdfView(request):
    y = 0
    #cuerpo = SolicitudDetalle.objects.filter(solicitud_id=cabeza.id)
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
    #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
    #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 16)
    #Dibujamos una cadena en la ubicación X,Y especificada
    y = 800
    x = 380
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(170, y, u""+empresa.nombre)
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(180, y, u"RECIBOS DE CAJA")
    pdf.setFont("Helvetica", 9)
    lista_id_recibos= request.session['lista_id_filtro_recibo_caja']
    if request.session['lista_id_filtro_recibo_caja']:
        id_recibos = request.session['lista_id_filtro_recibo_caja']
        recibos = ReciboCaja.objects.filter(id__in=id_recibos)
    else:
        recibos = ReciboCaja.objects.all()    
    total_reporte = 0    
    for i in recibos:
        y -= 15
        pdf.drawString(30,y , u"Fecha : "+i.fecha.strftime("%Y-%m-%d %H:%M:%S"))
        pdf.drawString(150, y, u"Número : "+i.numero)
        y -= 10
        pdf.drawString(30, y, u"Mesa   : "+str(i.IdMesa))
        pdf.drawString(150, y, u"Habitación   : "+str(i.IdHabitacion))
        y -= 10
        pdf.drawString(30, y, u"Pedido   : "+str(i.pedido_caja))
        if i.pagado == True:
            pdf.drawString(150, y, u"Pagado   : "+'Si')
        else:
            pdf.drawString(150, y, u"Pagado   : "+'No')
        y -=10        
        pdf.drawString(30,y, u'Producto                        Cantidad      Valor Unit.     Valor Total      Fecha/Hora')
        y -= 10
        total_recibo = 0
        recibo_caja_detalle = ReciboCajaDetalle.objects.filter(numero=i.numero)
        for i in recibo_caja_detalle:
            item = i.IdItem.descripcion[0:26]
            cantidad = str(i.cantidad)
            valor_unit = '{:,}'.format(i.valor)
            valor_total = '{:,}'.format(i.valor_total)
            fecha_hora = i.created.strftime("%Y-%m-%d %H:%M:%S")
            pdf.drawString(30,y , item[:26])
            pdf.drawString(140,y , cantidad)
            pdf.drawString(170,y , valor_unit)
            pdf.drawString(230,y , valor_total)
            pdf.drawString(280,y , fecha_hora)
            total_recibo = total_recibo + i.valor_total
            total_reporte = total_reporte + i.valor_total
            y -=10
            if y<= 40:
                pdf.showPage()
                y= 800
                pdf.setFont("Helvetica", 9)
        pdf.drawString(240, y, u"Total Recibo      : "+('{:,}'.format(total_recibo)+'.00'))
        y -=10
        pdf.line(30,y,x,y)
        y -= 10
    pdf.drawString(240, y, u"Total Reporte      : "+('{:,}'.format(total_reporte)+'.00'))    
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionRecibosCajaXlsView(request):
    #idrecibos = request.session['lista_id_filtro_recibo_caja']
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    #recibos_detalle = ReciboCajaDetalle.objects.filter(id=idsesionempaque)
    
    worksheet.write('A1','numero' )
    worksheet.write('B1','Fecha' )
    worksheet.write('C1','Cliente')
    worksheet.write('D1','Mesa')
    worksheet.write('E1','Habitación')
    worksheet.write('F1','Caja')
    worksheet.write('G1','Valor')
    worksheet.write('H1','Pagado')
    worksheet.write('I1','Usuario')
    #recibos = ReciboCaja.objects.filter(id__contains=idrecibos).order_by('numero')
    registros_filtro = request.session['lista_id_filtro_recibo_caja']
    if registros_filtro:
        #registros_filtro = request.session['lista_id_filtro_recibo_caja']
        recibos = ReciboCaja.objects.filter(id__in=registros_filtro)     
    else:
        recibos = ReciboCaja.objects.all()
    n=2
    for j in recibos:     
        nn = str(n)
        numero = j.numero
        fecha = j.fecha.strftime("%d/%m/%Y")
        cliente = j.IdTercero
        mesa = j.IdMesa
        habitacion = j.IdHabitacion
        caja = j.IdCaja
        valor = j.valor
        pagado = j.pagado
        usuario = j.IdUsuario   
        exec("worksheet.write('A"+nn+"','"+numero+"' )")
        exec("worksheet.write('B"+nn+"','"+str(fecha)+"' )")
        exec("worksheet.write('C"+nn+"','"+str(cliente)+"' )")
        exec("worksheet.write('D"+nn+"','"+str(mesa)+"' )")
        exec("worksheet.write('E"+nn+"','"+str(habitacion)+"' )")
        exec("worksheet.write('F"+nn+"','"+str(caja)+"' )")
        exec("worksheet.write('G"+nn+"','"+str(valor)+"' )")
        exec("worksheet.write('H"+nn+"','"+str(pagado)+"' )")
        exec("worksheet.write('I"+nn+"','"+str(usuario)+"' )")

        recibo_detalle = ReciboCajaDetalle.objects.filter(numero=j.numero)
        n +=1
        for i in recibo_detalle:
            mm = str(n)
            producto = i.IdItem
            cantidad = i.cantidad
            valor = i. valor
            valor_total = i.valor_total

            exec("worksheet.write('A"+mm+"','"+str(producto)+"' )")
            exec("worksheet.write('B"+mm+"','"+str(cantidad)+"' )")
            exec("worksheet.write('C"+mm+"','"+str(valor)+"' )")
            exec("worksheet.write('D"+mm+"','"+str(valor_total)+"' )") 
            n += 1
    n += 1
    workbook.close()
    output.seek(0)
    filename = 'recibos_caja.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    

def pedido_caja_detalle(pdf,idhabitacion_consolidar):
    response = HttpResponse(content_type='application/pdf')
    buffer = io.BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    archivo_imagen = settings.MEDIA_ROOT+'/img/logo_empresa.png'
    pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)
    pdf.setFont("Helvetica", 16)
    y = 770
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(170, y, u""+empresa.nombre)
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(200, y, u"PEDIDO")
    pdf.setFont("Helvetica", 9)
    if idhabitacion_consolidar == 99:
        pedidos = PedidoCaja.objects.filter(cerrado=0)
    else:
        pedidos = PedidoCaja.objects.filter(IdHabitacion_id=idhabitacion_consolidar)
    #cuerpo = SolicitudDetalle.objects.filter(solicitud_id=cabeza.id)
    numero_pedidos_cons = []
    for n in range(10):
        for i in pedidos:
            numero_pedidos_cons.append(i.numero)
            habitacion = Habitacion.objects.get(id=i.IdHabitacion_id )
            if habitacion.idHabitacion != '*':
                habitacion = Habitacion.objects.get(id=i.IdHabitacion_id )
                des_habitacion = habitacion.descripcion
            x = 380
            factor = 15
            baja = 5
            y -= 10
            pdf.line(30,y,x,y)
            y -= baja+5
            pdf.drawString(180,y , u"Fecha : "+timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
            y -= baja

            pdf.line(30,y,x,y)
            y -= baja
            y -= factor
            pdf.drawString(30, y, u"Habitación   : "+str(des_habitacion))
            y -= factor
            pdf.line(30,y,x,y)
            
            y = 700
            cuerpo = PedidoCajaDetalle.objects.filter(numero__in=numero_pedidos_cons)
            total_recibo = cuerpo.aggregate(Sum('valor_total'))['valor_total__sum']
            #total_pedido = f'{total_pedido}'
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
            if y<=15:
                pdf.showPage()
                y= 700    
            # Descontamos el encabezado
            y = y - 80
            # Restamos a y por cada fila de la grid
            y = y - b*18
            #Establecemos el tamaño de la hoja que ocupará la tabla
            detalle_recibo.wrapOn(pdf, 300, 800)
            #Definimos la coordenada donde se dibujará la tabla
            detalle_recibo.drawOn(pdf, 30,y)
            y -= 20
            if total_recibo:
                pdf.drawString(240, y, u"Total Recibo      : "+('{:,}'.format(total_recibo)+'.00'))
          
    return 

def impresion_cabeza_pedido_consolidado(pdf,pedidos,consolidar,idhabitacion_consolidar,y):
    if Habitacion.objects.filter(id=idhabitacion_consolidar ).exists():
        habitacion = Habitacion.objects.get(id=idhabitacion_consolidar )
        pdf.drawString(110, y, u"Habitación   : "+str(habitacion.descripcion))
    else:
        pdf.drawString(110, y, u"Habitación   : ")
    y -= 30

def impresion_cuerpo_pedido_consolidado(pdf,cuerpo,pedidos_cons,registros,y):
    if cuerpo:
        total_recibo = cuerpo.aggregate(Sum('valor_total'))['valor_total__sum']
        total = total_recibo
        encabezados = ('RecCaja','Producto', 'Cantidad', 'Valor Unit.', 'Valor Total','Fecha/Hora')
        detalles = [(cuerpo.numero,cuerpo.IdItem.descripcion[0:30], cuerpo.cantidad, '{:,}'.format(cuerpo.valor), '{:,}'.format(cuerpo.valor_total),cuerpo.created.strftime("%Y-%m-%d %H:%M:%S")) for cuerpo in cuerpo]
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
        b= 0
        print('Antes de cuerpo',y)
        print('Registros',registros)
        
        #Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_recibo.wrapOn(pdf, 300, 800)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_recibo.drawOn(pdf, 30,y)
        y -= 20
        pdf.setFont("Helvetica", 9)
        if total_recibo:
            pdf.drawString(240, y, u"Total Recibo      : "+('{:,}'.format(total_recibo)+'.00'))


def ImpresionPedidosCajaConsolidadoView(request):
    consolidar = request.session['consolidar']
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
    pdf.drawString(200, y, u"PEDIDO")
    pdf.setFont("Helvetica", 9)
    y -= 20
    x = 380
    numero_pedidos_cons = []
    if consolidar:
        idhabitacion_consolidar = request.session['id_habitacion_consolidar']
    pdf.line(30,y,x,y)
    y -= 10
    pdf.drawString(180,y , u"Fecha : "+timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    y -= 10
    pdf.line(30,y,x,y)
    y -= 10
    pedidos_cons = []
    if consolidar == False:
        if request.session['lista_id_filtro_pedido_caja']:
            lista_filtro_pedidos = request.session['lista_id_filtro_pedido_caja'] 
            pedidos = PedidoCaja.objects.filter(id__in=lista_filtro_pedidos)
        else:
            pedidos = PedidoCaja.objects.all().order_by('-numero')
        pedidos_cons = []
        for i in pedidos:
            cuerpo = PedidoCajaDetalle.objects.filter(numero=i.numero)
            registros = PedidoCajaDetalle.objects.filter(numero=i.numero).count()
            des_habitacion = i.IdHabitacion.descripcion
            pdf.drawString(30, y, u"Pedido   : "+str(i.numero))
            pdf.drawString(110, y, u"Habitación   : "+str(des_habitacion))
            y -= 25
            y = y -(registros*25)
            if y<=40:
                pdf.showPage()
                y= 750
            #impresion_cabeza_pedido_consolidado(pdf,pedidos,consolidar,idhabitacion_consolidar,y)    
            impresion_cuerpo_pedido_consolidado(pdf,cuerpo,pedidos_cons,registros,y)
            y -=40    
    else:
        idhabitacion_consolidar = request.session['id_habitacion_consolidar']
        pedidos = PedidoCaja.objects.filter(IdHabitacion_id=idhabitacion_consolidar,cerrado=False).order_by('-numero')    
        pedidos_cons = []
        for i in pedidos:
            pedidos_cons.append(i.numero)
        cuerpo = PedidoCajaDetalle.objects.filter(numero__in=pedidos_cons)    
        registros = PedidoCajaDetalle.objects.filter(numero__in=pedidos_cons).count()   
        impresion_cabeza_pedido_consolidado(pdf,pedidos,consolidar,idhabitacion_consolidar,y)
        y -= 25
        y = y -(registros*25)
        if y<=40:
            pdf.showPage()
            y= 750    
        impresion_cuerpo_pedido_consolidado(pdf,cuerpo,pedidos_cons,registros,y)     
          
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

#######################################################################

def impresion_pedido_caja(pdf,idpedidos_filtro,idcaja):
    y = 800
    #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 16)
    #Dibujamos una cadena en la ubicación X,Y especificada
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(140, y, u""+empresa.nombre)
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(160, y, u"PEDIDOS")
    pdf.setFont("Helvetica", 9)
    if idpedidos_filtro:
        pedidos = PedidoCaja.objects.filter(IdCaja_id=idcaja,id__in=idpedidos_filtro)
    else:
        pedidos = PedidoCaja.objects.filter(IdCaja_id=idcaja,id__in=idpedidos_filtro)    
    numero_pedidos_cons = []
    y -= 10
    x = 500
    for i in pedidos:
        #numero_pedidos_cons.append(i.numero)
        #pdf.line(30,y,x,y)
        y -= 10
        pdf.drawString(30,y , u"Fecha : "+i.fecha.strftime("%Y-%m-%d %H:%M:%S"))
        pdf.drawString(150, y, u"Número : "+i.numero)
        y -= 10
        pdf.drawString(30, y, u"Mesa   : "+str(i.IdMesa))
        pdf.drawString(150, y, u"Habitación   : "+str(i.IdHabitacion))
        y -= 10
        cuerpo = PedidoCajaDetalle.objects.filter(numero=i.numero)
        registros = PedidoCajaDetalle.objects.filter(numero=i.numero).count()
        total_recibo = cuerpo.aggregate(Sum('valor_total'))['valor_total__sum']
        encabezados = ('Producto', 'Cantidad', 'Valor Unit.', 'Valor Total','Fecha/Hora')
        detalles = [(cuerpo.IdItem.descripcion[0:30], cuerpo.cantidad, '{:,}'.format(cuerpo.valor), '{:,}'.format(cuerpo.valor_total),cuerpo.created.strftime("%Y-%m-%d %H:%M:%S")) for cuerpo in cuerpo]
        detalle_recibo = Table([encabezados] + detalles, colWidths=[4 * cm, 1.1 * cm, 1.7 * cm, 2 * cm,2.7 * cm])
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
        y = y-20
        y = y -(registros*23)
        if y<=40:
           pdf.showPage()
           y= 750 
        detalle_recibo.wrapOn(pdf, 300, 800)
        detalle_recibo.drawOn(pdf, 30,y)
        y -= 15
        if total_recibo:
            pdf.setFont("Helvetica", 9)
            pdf.drawString(240, y, u"Total Recibo      : "+('{:,}'.format(total_recibo)+'.00'))
        y -= 10
        
    return



""" def ImpresionPedidosCajaView(request):
    y = 0
    #cabeza = ReciboCaja.objects.filter(id=id)
    #cuerpo = SolicitudDetalle.objects.filter(solicitud_id=cabeza.id)
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    idpedidos_cons = request.session['lista_id_filtro_pedido_caja']
    print
    if idpedidos_cons !='':
        impresion_pedido_caja(pdf,idpedidos_cons)
    else:
        idpedidos_filtro = request.session['lista_id_filtro_pedido_caja']
        impresion_pedido_caja(pdf,idpedidos_filtro)
    #Con show page hacemos un corte de página para pasar a la siguiente
    y = 455
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response """

def ImpresionPedidoCajaDetalleView(default,id):
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    y = 800
    #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 16)
    #Dibujamos una cadena en la ubicación X,Y especificada
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(120, y, u""+empresa.nombre)
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(130, y, u"DETALLE PEDIDO")
    pdf.setFont("Helvetica", 9)
    pedido = PedidoCaja.objects.get(id=id)
    y -= 10
    x = 350
    pdf.line(30,y,x,y)
    y -= 20
    pdf.drawString(30,y , u"Fecha : "+pedido.fecha.strftime("%Y-%m-%d %H:%M:%S"))
    pdf.drawString(150, y, u"Número : "+pedido.numero)
    y -= 10
    pdf.drawString(30, y, u"Mesa   : "+str(pedido.IdMesa))
    pdf.drawString(150, y, u"Habitación   : "+str(pedido.IdHabitacion))
    y -= 35
    cuerpo = PedidoCajaDetalle.objects.filter(numero=pedido.numero)
    total_recibo = cuerpo.aggregate(Sum('valor_total'))['valor_total__sum']
    encabezados = ('Producto', 'Cantidad', 'Valor Unit.', 'Valor Total','Fecha/Hora')
    detalles = [(cuerpo.IdItem.descripcion[0:40], cuerpo.cantidad, '{:,}'.format(cuerpo.valor), '{:,}'.format(cuerpo.valor_total),cuerpo.created.strftime("%Y-%m-%d %H:%M:%S")) for cuerpo in cuerpo]
    detalle_recibo = Table([encabezados] + detalles, colWidths=[4 * cm, 1.2 * cm, 2.0 * cm, 2.0 * cm,cm * 2.5])
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
    for j in cuerpo:
        b += 1
    y = y - b*25
    if y<=15:
        pdf.showPage()
        y = 800
    detalle_recibo.wrapOn(pdf, 300, 800)
    detalle_recibo.drawOn(pdf, 30,y)
    y -= 10
    pdf.setFont("Helvetica", 9)
    pdf.drawString(240, y, u"Total Recibo      : "+('{:,}'.format(total_recibo)+'.00'))
    y -= 20
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)    
    return response

def ImpresionPedidosCajaPdfView(request):
    y = 0
    #cabeza = ReciboCaja.objects.filter(id=id)
    #cuerpo = SolicitudDetalle.objects.filter(solicitud_id=cabeza.id)
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    #idpedidos_cons = request.session['idpedidos_cons']
    idcaja = request.session['idcaja']
    idpedidos_cons = request.session['lista_id_filtro_pedido_caja']
    impresion_pedido_caja(pdf,idpedidos_cons,idcaja)
    #Con show page hacemos un corte de página para pasar a la siguiente
    y = 455
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
    
def ImpresionPedidosCajaXlsView(request):
    #idrecibos = request.session['lista_id_filtro_recibo_caja']
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    #recibos_detalle = ReciboCajaDetalle.objects.filter(id=idsesionempaque)
    
    worksheet.write('A1','numero' )
    worksheet.write('B1','Fecha' )
    worksheet.write('C1','Caja')
    worksheet.write('D1','Mesa')
    worksheet.write('E1','Habitación')
    worksheet.write('F1','Recibo Caja')
    worksheet.write('G1','Valor')
    worksheet.write('H1','Usuario')
    idcaja = request.session['idcaja']
    registros_filtro = request.session['lista_id_filtro_pedido_caja']
    if registros_filtro:
        pedidos = PedidoCaja.objects.filter(id__in=registros_filtro)     
    else:
        pedidos = PedidoCaja.objects.all(IdCaja_id=idcaja)
    pedidos_reg=[]
    for j in pedidos:
        pedidos_reg.append(j.numero)
    cuerpo = PedidoCajaDetalle.objects.filter(numero__in=pedidos_reg)
    total_pedido = cuerpo.aggregate(Sum('valor_total'))['valor_total__sum']
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
    n += 1
    workbook.close()
    output.seek(0)
    filename = 'pedidos_caja.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    

def ImpresionPedidosCajaConsolidadoXlsView(request):
    #idrecibos = request.session['lista_id_filtro_recibo_caja']
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    #recibos_detalle = ReciboCajaDetalle.objects.filter(id=idsesionempaque)
    
    worksheet.write('A1','numero' )
    worksheet.write('B1','Fecha' )
    worksheet.write('C1','Caja')
    worksheet.write('D1','Mesa')
    worksheet.write('E1','Habitación')
    worksheet.write('F1','Recibo Caja')
    worksheet.write('G1','Valor')
    worksheet.write('H1','Usuario')
    idcaja = request.session['idcaja']
    registros_filtro = request.session['lista_id_filtro_pedido_caja']
    if registros_filtro:
        pedidos = PedidoCaja.objects.filter(id__in=registros_filtro)     
    else:
        pedidos = PedidoCaja.objects.all(IdCaja_id=idcaja)
    if request.session['consolidar']:
        #idhabitacion_consolidar = request.session['id_habitacion_consolidar']
        listra_reg =request.session['lista_id_filtro_pedido_caja']
        #pedidos = PedidoCaja.objects.filter(IdHabitacion_id=idhabitacion_consolidar,cerrado=False)
        #pedidos = PedidoCaja.objects.filter(IdHabitacion_id=idhabitacion_consolidar,cerrado=False,id__in=listra_reg)
        pedidos = PedidoCaja.objects.filter(cerrado=False,id__in=listra_reg)
    pedidos_reg = []
    for j in pedidos:
        pedidos_reg.append(j.numero)
    cuerpo = PedidoCajaDetalle.objects.filter(numero__in=pedidos_reg)
    total_pedido = cuerpo.aggregate(Sum('valor_total'))['valor_total__sum']
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
            idhabitacion_consolidar = request.session['id_habitacion_consolidar']
            habitacion = Habitacion.objects.get(id=idhabitacion_consolidar)
            exec("worksheet.write('E"+nn+"','"+str(habitacion.descripcion)+"' )")
            exec("worksheet.write('G"+nn+"','"+str(total_pedido)+"' )")
            exec("worksheet.write('H"+nn+"','"+str(usuario)+"' )")
            sw = 1
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
            if request.session['consolidar'] == True:
                tw = 1  
         
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
    n += 1
    workbook.close()
    output.seek(0)
    filename = 'pedidos_caja.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    

def ImpresionPedidosCajaTodosXlsView(request):
    #idrecibos = request.session['lista_id_filtro_recibo_caja']
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    #recibos_detalle = ReciboCajaDetalle.objects.filter(id=idsesionempaque)
    
    worksheet.write('A1','numero' )
    worksheet.write('B1','Fecha' )
    worksheet.write('C1','Caja')
    worksheet.write('D1','Mesa')
    worksheet.write('E1','Habitación')
    worksheet.write('F1','Recibo Caja')
    worksheet.write('G1','Valor')
    worksheet.write('H1','Usuario')
    #recibos = ReciboCaja.objects.filter(id__contains=idrecibos).order_by('numero')
    idpedidos_filtro = request.session['lista_id_filtro_pedido_caja']
    if idpedidos_filtro !=[]:
        pedidos = PedidoCaja.objects.filter(id__in=idpedidos_filtro)
    else: 
        pedidos = PedidoCaja.objects.all()
    list_numero = []
    for t in pedidos:
        list_numero.append(t.numero)
    pedido_detalle = PedidoCajaDetalle.objects.filter(numero__in=list_numero)
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
        total_pedido = pedido_detalle.aggregate(Sum('valor_total'))['valor_total__sum']       
        if sw == 0:
            if request.session['consolidar'] == False:   
                exec("worksheet.write('A"+nn+"','"+numero+"' )")
                exec("worksheet.write('B"+nn+"','"+str(fecha)+"' )")
                exec("worksheet.write('C"+nn+"','"+str(caja)+"' )")
                exec("worksheet.write('D"+nn+"','"+str(mesa)+"' )")
                exec("worksheet.write('E"+nn+"','"+str(habitacion)+"' )")
                exec("worksheet.write('F"+nn+"','"+str(recibo_caja)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(valor_total)+"' )")
            else:
                idhabitacion_consolidar = request.session['id_habitacion_consolidar']
                habitacion = Habitacion.objects.get(id=idhabitacion_consolidar)
                exec("worksheet.write('E"+nn+"','"+str(habitacion.descripcion)+"' )")
                exec("worksheet.write('G"+nn+"','"+str(total_pedido)+"' )")
                exec("worksheet.write('H"+nn+"','"+str(usuario)+"' )")
                sw = 1
        pedido_detalle = PedidoCajaDetalle.objects.filter(numero=j.numero)
        n +=1
        mm = str(n)
        if tw == 0:
            exec("worksheet.write('A"+mm+"','numero' )")
            exec("worksheet.write('B"+mm+"','Producto' )")
            exec("worksheet.write('C"+mm+"','Cantidad' )")
            exec("worksheet.write('D"+mm+"','Valor' )")
            exec("worksheet.write('E"+mm+"','Valor Total' )")
            exec("worksheet.write('F"+mm+"','Fecha' )")
            n +=1
            if request.session['consolidar'] == True:
                tw = 1  
         
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
            exec("worksheet.write('F"+mm+"','"+str(valor_total)+"' )")
            exec("worksheet.write('F"+mm+"','"+str(fecha)+"' )") 
            n += 1
    n += 1
    workbook.close()
    output.seek(0)
    filename = 'pedidos_caja.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    

def ImpresionPedidoCajaDetalleXlsView(request,id):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
       
    worksheet.write('A1','numero' )
    worksheet.write('B1','Fecha' )
    worksheet.write('C1','Caja')
    worksheet.write('D1','Mesa')
    worksheet.write('E1','Habitación')
    worksheet.write('F1','Valor')
    worksheet.write('G1','recibo Caja')
    worksheet.write('H1','Usuario')
    
    pedido = PedidoCaja.objects.get(id=id)     
    numero = pedido.numero
    fecha = pedido.fecha.strftime("%d/%m/%Y")
    caja = pedido.IdCaja
    mesa = pedido.IdMesa
    habitacion = pedido.IdHabitacion
    valor_total = pedido.valor_total
    recibo_caja = pedido.recibo_caja
    usuario = pedido.IdUsuario
    n = 2
    nn = str(n)    
    exec("worksheet.write('A"+nn+"','"+numero+"' )")
    exec("worksheet.write('B"+nn+"','"+str(fecha)+"' )")
    exec("worksheet.write('C"+nn+"','"+str(caja)+"' )")
    exec("worksheet.write('D"+nn+"','"+str(mesa)+"' )")
    exec("worksheet.write('E"+nn+"','"+str(habitacion)+"' )")
    exec("worksheet.write('F"+nn+"','"+str(valor_total)+"' )")
    exec("worksheet.write('G"+nn+"','"+str(recibo_caja)+"' )")
    exec("worksheet.write('H"+nn+"','"+str(usuario)+"' )")
        
    pedido_detalle = PedidoCajaDetalle.objects.filter(numero=pedido.numero)
    worksheet.write('A3','Producto' )
    worksheet.write('B3','Cantidad' )
    worksheet.write('C3','Valor')
    worksheet.write('D3','Valor Total')
    worksheet.write('E3','Fecha/Hora')
    n = 4
    for i in pedido_detalle:
        mm = str(n)
        producto = i.IdItem
        cantidad = i.cantidad
        valor = i. valor
        valor_total = i.valor_total
        fecha = i.created.strftime("%Y-%m-%d %H:%M:%S")
        exec("worksheet.write('A"+mm+"','"+str(producto)+"' )")
        exec("worksheet.write('B"+mm+"','"+str(cantidad)+"' )")
        exec("worksheet.write('C"+mm+"','"+str(valor)+"' )")
        exec("worksheet.write('D"+mm+"','"+str(valor_total)+"' )")
        exec("worksheet.write('E"+mm+"','"+str(fecha)+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'pedido_caja_detalle.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    

def impresion_pedido_caja_todos(pdf,idpedidos_filtro):
    y = 800
    #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
    pdf.setFont("Helvetica", 16)
    #Dibujamos una cadena en la ubicación X,Y especificada
    empresa = Empresa.objects.get(id=1)
    pdf.drawString(170, y, u""+empresa.nombre)
    pdf.setFont("Helvetica", 14)
    y -= 20
    pdf.drawString(200, y, u"PEDIDOS")
    pdf.setFont("Helvetica", 9)
    if idpedidos_filtro !=[]:
        pedidos = PedidoCaja.objects.filter(id__in=idpedidos_filtro)
    else: 
        pedidos = PedidoCaja.objects.all()
    numero_pedidos_cons = []
    y -= 10
    x = 380
    b=0
    for i in pedidos:
        numero_pedidos_cons.append(i.numero)
        y -= 10
        pdf.drawString(30,y , u"Fecha : "+i.fecha.strftime("%Y-%m-%d %H:%M:%S"))
        pdf.drawString(150, y, u"Número : "+i.numero)
        y -= 10
        pdf.drawString(30, y, u"Mesa   : "+str(i.IdMesa))
        pdf.drawString(150, y, u"Habitación   : "+str(i.IdHabitacion))
        y -= 10
        cuerpo = PedidoCajaDetalle.objects.filter(numero=i.numero)
        total_recibo = 0
        pdf.drawString(30,y, u'Producto                        Cantidad      Valor Unit.     Valor Total         Fecha/Hora')
        y -= 10
        for i in cuerpo:
            item = i.IdItem.descripcion
            cantidad = str(i.cantidad)
            valor_unit = '{:,}'.format(i.valor)
            valor_total = '{:,}'.format(i.valor_total)
            fecha_hora = i.created.strftime("%Y-%m-%d %H:%M:%S")
            pdf.drawString(30,y , item[:26])
            pdf.drawString(142,y , cantidad)
            pdf.drawString(170,y , valor_unit)
            pdf.drawString(230,y , valor_total)
            pdf.drawString(280,y , fecha_hora)
            total_recibo = total_recibo + i.valor_total
            b = b + 1
            y -=10
            if y<= 40:
                pdf.showPage()
                y= 800
                pdf.setFont("Helvetica", 9)
        pdf.drawString(240, y, u"Total Recibo      : "+('{:,}'.format(total_recibo)+'.00'))
        y -=10
        pdf.line(30,y,x,y)
        y -= 10
     
    return

def ImpresionPedidosCajaTodosPdfView(request):
    y = 0
    #cabeza = ReciboCaja.objects.filter(id=id)
    #cuerpo = SolicitudDetalle.objects.filter(solicitud_id=cabeza.id)
    #Indicamos el tipo de contenido a devolver, en este caso un pdf
    response = HttpResponse(content_type='application/pdf')
    #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
    buffer = io.BytesIO()
    #Canvas nos permite hacer el reporte con coordenadas X y Y
    pdf = canvas.Canvas(buffer)
    #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
    idpedidos_list = request.session['lista_id_filtro_pedido_caja']
    impresion_pedido_caja_todos(pdf,idpedidos_list)
    #Con show page hacemos un corte de página para pasar a la siguiente
    y = 455
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
    
def ImpresionPagosCajaXlsView(request):
    #print('Recibos: ',request.session['lista_id_filtro_pago_caja'])
    #idrecibos = request.session['lista_id_filtro_recibo_caja']
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    #recibos_detalle = ReciboCajaDetalle.objects.filter(id=idsesionempaque)
    
    worksheet.write('A1','numero' )
    worksheet.write('B1','Fecha' )
    worksheet.write('C1','Caja')
    worksheet.write('D1','Recibo Caja')
    worksheet.write('E1','Tipo Pago')
    worksheet.write('F1','Tarjeta Crédito')
    worksheet.write('G1','Valor')
    worksheet.write('H1','Usuario')
    #recibos = ReciboCaja.objects.filter(id__contains=idrecibos).order_by('numero')
    registros_filtro = request.session['lista_id_filtro_pago_caja']
    if registros_filtro:
        #registros_filtro = request.session['lista_id_filtro_recibo_caja']
        pagos = PagoReciboCaja.objects.filter(id__in=registros_filtro)     
    else:
        pagos = PagoReciboCaja.objects.all()
    n=2
    for j in pagos:     
        nn = str(n)
        numero = j.numero
        fecha = j.fecha.strftime("%d/%m/%Y")
        caja = j.IdCaja
        recibo_caja = j.recibo_caja
        tipo_pago = j.IdTipoPago
        tarjeta = j.IdTarjetaCredito
        valor = j.valor
        usuario = j.IdUsuario   
        exec("worksheet.write('A"+nn+"','"+numero+"' )")
        exec("worksheet.write('B"+nn+"','"+str(fecha)+"' )")
        exec("worksheet.write('C"+nn+"','"+str(caja)+"' )")
        exec("worksheet.write('D"+nn+"','"+str(recibo_caja)+"' )")
        exec("worksheet.write('E"+nn+"','"+str(tipo_pago)+"' )")
        exec("worksheet.write('F"+nn+"','"+str(tarjeta)+"' )")
        exec("worksheet.write('G"+nn+"','"+str(valor)+"' )")
        exec("worksheet.write('H"+nn+"','"+str(usuario)+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'pagos_caja.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from  reportlab.lib.styles import ParagraphStyle

style = getSampleStyleSheet()['Normal']

def P(txt):
    return Paragraph(txt, style)

style = ParagraphStyle(
    name='Normal',
    fontSize=7,
    )


def ImpresionPagosCajaView(request):
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
    pdf.drawString(250, y, u"PAGOS")
    #pdf.setFont("Helvetica", 9)
    lista_id = request.session['lista_id_filtro_pago_caja']
    if lista_id:
        pagos = PagoReciboCaja.objects.filter(id__in=lista_id)
    else:
        pagos = PagoReciboCaja.objects.all()    
    y -= 20
    #y -= 20
    encabezados = ('Número','Fecha','Detalle','Caja','Cliente','Rec. Caja','Tipo Pago','Tarjeta Cred.','Valor')
    detalle = [(pago.numero, pago.fecha,P(pago.detalle),P(pago.IdCaja.descripcion),P(pago.IdTercero.apenom),pago.recibo_caja,P(pago.IdTipoPago.descripcion),P(pago.IdTarjetaCredito.descripcion),'{:,}'.format(pago.valor)) for pago in pagos]
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

def ImpresionPagosCajaTodosPdfView(request):
    y = 0
    x = 500
    response = HttpResponse(content_type='application/pdf')
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    y = 800
    empresa = Empresa.objects.get(id=1)
    pdf.setFont("Helvetica", 14)
    pdf.drawString(210, y, u""+empresa.nombre)
    y -= 15
    pdf.drawString(250, y, u"PAGOS")
    lista_id = request.session['lista_id_filtro_pago_caja']
    if lista_id:
        pagos = PagoReciboCaja.objects.filter(id__in=lista_id)
    else:
        pagos = PagoReciboCaja.objects.all()    
    y -= 20
    pdf.setFont("Helvetica", 9)
    
    total_reporte = 0
    for i in pagos:
        pdf.drawString(30,y, u' Fecha             Número           Caja                                                 Cliente')
        y -= 15
        pdf.drawString(30,y , u""+i.fecha.strftime("%Y-%m-%d"))
        pdf.drawString(90, y, u""+i.numero)
        pdf.drawString(140, y, u""+str(i.IdCaja))
        pdf.drawString(250, y, u""+str(i.IdTercero))
        y -= 10
        pdf.drawString(30, y, u"Recibo de Caja: "+str(i.recibo_caja))
        pdf.drawString(150, y, u"Tipo Pago: "+str(i.IdTipoPago))
        pdf.drawString(280, y, u"Tarjeta: "+str(i.IdTarjetaCredito))
        pdf.drawString(400, y, u"Valor: "+('{:,}'.format(i.valor)+'.00'))
        total_reporte = total_reporte + i.valor
        y -= 10
        pdf.line(30,y,x,y)
        y -= 10
        if y<= 40:
           pdf.showPage()
           y= 800
           pdf.setFont("Helvetica", 9)
    pdf.drawString(360, y, u"Total Reporte      : "+('{:,}'.format(total_reporte)+'.00'))    
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def ImpresionCuadreCajaXlsView(request,idcaja):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    idcaja = int(idcaja)
    caja = Caja.objects.get(id=idcaja)
    fecha =request.session['fecha_cuadre_caja']
    pago = PagoReciboCaja.objects.filter(fecha=fecha,IdCaja_id=idcaja).values('IdTipoPago','IdTipoPago__descripcion').annotate(total_valor=Sum('valor')).order_by('IdTipoPago__descripcion')        
    n = 1
    worksheet.write('A1','Fecha' )
    worksheet.write('B1','Caja' )
    worksheet.write('C1','Tipo Pago')
    worksheet.write('D1','Valor')
    worksheet.write('E1','Total Caja')
    total = 0
    for j in pago:     
        nn = str(n)
        tipo_pago = str(j['IdTipoPago__descripcion'])
        #tipo_pago = j.IdTipopago__descripcion
        valor = ('{:,}'.format(j['total_valor'])+'.00')
        total = total+j['total_valor']   
        exec("worksheet.write('A"+nn+"','"+fecha+"' )")
        exec("worksheet.write('B"+nn+"','"+caja.descripcion+"' )")
        exec("worksheet.write('C"+nn+"','"+tipo_pago+"' )")
        exec("worksheet.write('D"+nn+"','"+valor+"' )")
        n += 1
    total = ('{:,}'.format(total)+'.00')
    exec("worksheet.write('E"+nn+"','"+total+"' )")
    workbook.close()
    output.seek(0)
    filename = 'cuadre_caja.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    

def ImpresionCuadreCajaView(request,idcaja):
    idcaja = int(idcaja)
    caja = Caja.objects.get(id=idcaja)
    fecha =request.session['fecha_cuadre_caja']
    pago = PagoReciboCaja.objects.filter(fecha=fecha,IdCaja_id=idcaja).values('IdTipoPago','IdTipoPago__descripcion').annotate(total_valor=Sum('valor')).order_by('IdTipoPago__descripcion')        
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
    pdf.drawString(230, y, u"CUADRE CAJA")
    pdf.setFont("Helvetica", 12)
    y -= 90
    pdf.drawString(33,y , u"FECHA")
    pdf.drawString(110, y, u"CAJA")
    pdf.drawString(220, y, u"TIPO PAGO")
    pdf.drawString(350, y, u"VALOR")
    total = 0
    print(pago)
    for i in pago:
        y -= 20
        pdf.line(30,y,450,y)
        y -= 20
        pdf.drawString(30,y , u""+fecha)
        pdf.drawString(115, y, u""+caja.descripcion)
        pdf.drawString(210, y, u""+str(i['IdTipoPago__descripcion']))
        pdf.drawString(355, y, u""+('{:,}'.format(i['total_valor'])+'.00'))
        total = total+i['total_valor']
    y -= 15
    pdf.line(30,y,450,y)
    y -= 15
    pdf.setFont("Helvetica", 12)
    pdf.drawString(260, y, u"Total Recibo        "+('{:,}'.format(total)+'.00'))
    
    pdf.showPage()   
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

def SwFiltroReciboCaja(request):
    request.session['sw_filtro_recibo_caja'] = True
    print('Filtro 2 :',request.session['sw_filtro_recibo_caja'])
    data = {'id':0}
    return JsonResponse(data) 


def SwFiltroReciboCaja(request):
    request.session['sw_filtro_recibo_caja'] = True
    print('Filtro 2 :',request.session['sw_filtro_recibo_caja'])
    data = {'id':0}
    return JsonResponse(data) 


def SubeTerceros(request):
    servidor = 'DESKTOP-5I8FNLC\SQLEXPRESS'  # Nombre del servidor SQL con el cual se hará la conexión
    bddatos = 'TEJIDOS'  # Nombre de la base de datos SQL
    usuario = 'sa' # Nombre del usuario de SQL
    clave = 'JJGUEVARA'  # Contraseña del usuario de SQL
    connectionString = 'DRIVER=SQL Server Native Client 11.0;Server=DESKTOP-5I8FNLC\SQLEXPRESS;Database=tejidos;'+'UID='+usuario+';PWD='+clave
    print(connectionString)
    
    try:
        conexion = pyodbc.connect(connectionString)
        print("conexión exitosa")
    except:
        print('No Se Pudo Hacer la Conexion') 

    query = "select * from Terceros where idtipoidentificacion=13 "
    cursor = conexion.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    tercero = Tercero()
    n = 0
    for row in rows:
        n = n+1
        sn = str(n)
        numero = sn.zfill(8)
        print(numero)
        
        idTercero= numero 
        tipoidentificacion = 6
        idtipoTercero = 1
        numero_identificacion = row[2]
        nombre1 =row[5]
        nombre2 =row[6]
        apel1 = row[7]
        apel2 = row[8]
        apenom = row[9]
        razon_social = apenom
        idpais = 2
        iddepartamento = 3
        idciudad= 2
        direccion=row[21]
        telefonos=row[22]
        email=row[25]
        contacto =''
        IdUsuario = request.user.id
        #1
        tercero.idTercero =  numero
        #2
        tercero.IdTipoIdentificacion_id = tipoidentificacion
        #3
        
        tercero.identificacion= numero_identificacion
        #5
        tercero.razon_social = razon_social
        #6
        tercero.nombre1 = nombre1
        #7
        tercero.nombre2 = nombre2
        #8
        tercero.apel1 = apel1
        #9
        tercero.apel2 = apel2
        #10
        tercero.nombre = apenom

        #11
        #12
        tercero.IdPais_id = idpais
        #13
        tercero.IdDepartamento_id = iddepartamento
        #14
        tercero.IdCiudad_id = idciudad
        #15
        #16
        #17 
        #22
        tercero.direccion = direccion
        #23
        tercero.telefono = telefonos
        #26
        tercero.email = email
        #27
        #especial
        #28
        tercero.IdUsuario_id = request.user.id
        tercero.save()       
        tercero.id = tercero.id+1


