from django.shortcuts import render

# Create your views here.
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
#import xlsxwriter

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
from datetime import timedelta
import xlsxwriter
from io import BytesIO
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter, landscape, A4
#from django.conf import settings
#from reportlab.platypus import Paragraph, Table, TableStyle
#from reportlab.lib import colors
#from reportlab.lib.units import inch, cm
#from reportlab.lib.enums import TA_JUSTIFY
#from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
#from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#from reportlab.lib.units import mm
import io
from django.http import FileResponse
import csv
from django.db.models import Subquery

from django.contrib.auth.mixins import LoginRequiredMixin
#from reportlab.platypus.tables import LINEJOINS

from django.contrib import messages

from decimal import Decimal

from django.template.loader import render_to_string

import json

from django.shortcuts import render, redirect

#from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from django.core import serializers
from django.core.serializers import serialize

from core.models import Tercero,TipoIdentificacion,Ciudad,Pais,Departamento,Sucursal,ValorDefecto
from core.tables import TercerosTable1,TercerosTable2
from core.forms import TerceroForm
from core.filters import TerceroFilter1 

from django import forms

from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.core.paginator import Paginator

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "core/wellcome.html")
    # En otro caso redireccionamos al login
    return redirect('users/login')

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/register.html", {'form': form})

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

class HomePageView(TemplateView):
    template_name = "core/home.html"
    
class MenuHotel(TemplateView):
    template_name = "hotel/menu_hotel.html"

class MenuCaja(TemplateView):
    template_name = "caja/menu_caja.html"

class MenuRecibosCaja(TemplateView):
    template_name = "caja/menu_recibos_caja.html"

class MenuCompras(TemplateView):
    template_name = "compras/menu_compras.html"

class MenuCxC(TemplateView):
    template_name = "cxc/menu_cxc.html"

class MenuCxP(TemplateView):
    template_name = "cxp/menu_cxp.html"

class MenuInventarios(TemplateView):
    template_name = "inventarios/menu_inventarios.html"

class MenuTesoreria(TemplateView):
    template_name = "tesoreria/menu_tesoreria.html"    

class MenuVentas(TemplateView):
    template_name = "ventas/menu_ventas.html"    

class MenuProcesos(TemplateView):
    template_name = "core/menu_procesos.html"

class MenuCocina(TemplateView):
    template_name = "cocina/menu_cocina.html"   
    
""" def TerceroListView(request):
    terceros = TercerosTable(Tercero.objects.all())
    terceros.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'terceros':terceros}
    return render(request, 'core/terceros_lista.html', context) 
 """

def TerceroListView(request):
    queryset = Tercero.objects.all()
    f =  TerceroFilter1 (request.GET, queryset=queryset)
    terceros = TercerosTable1(f.qs)
    request.session['lista_filtro_id_terceros'] = False
    lista_id = []
    for n in f.qs:
        lista_id.append(n.id)
        request.session['lista_filtro_id_terceros']  = lista_id
    terceros.paginate(page=request.GET.get("page", 1), per_page=12)
    context = {'terceros':terceros,'filter':f}
    return render(request, 'core/terceros_lista.html', context) 


def DetalleTerceroView(request,id):
    terceros1 = TercerosTable1(Tercero.objects.filter(id=id))
    terceros2 = TercerosTable2(Tercero.objects.filter(id=id))
    context = {'terceros1':terceros1,'terceros2':terceros2}
    return render(request, 'core/detalle_terceros_lista.html', context) 


class CreaTerceroView(LoginRequiredMixin,CreateView):
    model = Tercero
    template_name = 'core/tercero_form.html'
    form_class = TerceroForm
    
    def get_success_url(self):
        return reverse_lazy('terceros_list')
    
    def get_initial(self,*args,**kwargs):
        initial=super(CreaTerceroView,self).get_initial(**kwargs)
        valor_defecto_pais = ValorDefecto.objects.get(idValor='02')
        pais = Pais.objects.get(idPais=valor_defecto_pais.valor)
        initial['IdPais'] = pais.id
        return initial
    
    def form_valid(self, form):
        if form.is_valid():
            tercero = form.save(commit=False)
            #tipoter = TipoTercero.objects.get(id=1)
            #tercero.IdTipoTercero_id = tipoter.id 
            registros = Tercero.objects.count()
            sregistro= str(registros+1)
            idtercero = sregistro.zfill(8)
            tercero = form.save(commit=False)
            tercero.idTercero = idtercero
            tercero.IdUsuario_id = self.request.user.id
            tercero.save()
            idtercero = Tercero.objects.latest('id')
            tercero = Tercero.objects.get(id=idtercero.id)
            self.request.session['idtercero' ] = tercero.id
            print('Tercero Id:',tercero.id)
            Tercero.objects.filter(id=idtercero.id).update(apenom = tercero.apel1.strip()+" "+tercero.apel2.strip()+" "+tercero.nombre1.strip()+" "+tercero.nombre2.strip())
            return redirect('terceros_list')   


class EditaTerceroView(LoginRequiredMixin,UpdateView):
    model = Tercero
    fields = ['identificacion','IdTipoIdentificacion','identifica_de','nombre1','nombre2','apel1','apel2','razon_social','IdPais','departamento','ciudad',
                  'direccion','telefono','email','ocupacion','direccion','telefono','email','contacto','por_ica','por_ret_fte']
    template_name = 'core/tercero_form.html'
    #success_url = reverse_lazy('terceros_list')

    def get_success_url(self):
        pk = self.kwargs["pk"]
        Tercero.objects.filter(id=pk).update(apenom= self.object.apel1.strip()+" "+self.object.apel2.strip()+" "+self.object.nombre1.strip()+" "+self.object.nombre2.strip()   )
        return reverse("terceros_list")
    
class BorraTerceroView(LoginRequiredMixin,DeleteView):
    model = Tercero
    success_url = reverse_lazy('terceros_list')
    template_name = 'core/confirma_borrado.html'

def ImpresionTercerosXlsView(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    
    #identificacion','IdTipoIdentificacion','identifica_de','nombre1','nombre2','apel1','apel2','razon_social','nombre','direccion','telefono','email','ocupacion',
    #'IdPais','departamento','ciudad','contacto','por_ica','por_ret_fte'
    worksheet.write('A1','Identificacion' )
    worksheet.write('B1','Tipo Identificacion' )
    worksheet.write('C1','Identifica De' )
    worksheet.write('D1','Nombre 1' )
    worksheet.write('E1','Nombre 2' )
    worksheet.write('F1','Apellido 1' )
    worksheet.write('G1','Apellido 2' )
    worksheet.write('H1','Razon Social' )
    worksheet.write('I1','Nombre' )
    worksheet.write('J1','Direccion' )
    worksheet.write('K1','Telefono' )
    worksheet.write('L1','Email' )
    worksheet.write('M1','Ocupacion' )
    worksheet.write('N1','Pais' )
    worksheet.write('O1','Departamento' )
    worksheet.write('P1','Ciudad' )
    worksheet.write('Q1','Contacto' )
    worksheet.write('R1','Por Ica' )
    worksheet.write('S1','Por Ret Fte' )
    id_registros = request.session['lista_id_terceros']
    n = 2
    if request.session['lista_filtro_id_terceros']:
        id_terceros = request.session['lista_filtro_id_terceros']       
        terceros =Tercero.objects.filter(id__in=id_terceros)
    else:
        terceros = Tercero.objects.all()    
    for j in terceros: 
        nn = str(n)
        pais = j.IdPais.descripcion
        if j.razon_social == None:
            razon_social = ''
        else:
            razon_social = j.razon_social    
        exec("worksheet.write('A"+nn+"','"+j.identificacion+"' )")
        exec("worksheet.write('B"+nn+"','"+j.IdTipoIdentificacion.descripcion+"' )")
        exec("worksheet.write('C"+nn+"','"+j.identifica_de+"' )")
        exec("worksheet.write('D"+nn+"','"+j.nombre1+"' )")
        exec("worksheet.write('E"+nn+"','"+j.nombre2+"' )")
        exec("worksheet.write('F"+nn+"','"+j.apel1+"' )")
        exec("worksheet.write('G"+nn+"','"+j.apel2+"' )")
        exec("worksheet.write('H"+nn+"','"+razon_social+"' )")
        exec("worksheet.write('I"+nn+"','"+j.apel1.strip()+" "+j.apel2.strip()+" "+j.nombre1.strip()+" "+j.nombre2.strip()+"' )")
        exec("worksheet.write('J"+nn+"','"+j.direccion+"' )")
        exec("worksheet.write('K"+nn+"','"+j.telefono+"' )")
        exec("worksheet.write('L"+nn+"','"+str(j.email)+"' )")
        exec("worksheet.write('M"+nn+"','"+j.ocupacion+"' )")
        exec("worksheet.write('N"+nn+"','"+pais+"' )")
        exec("worksheet.write('O"+nn+"','"+j.departamento+"' )")
        exec("worksheet.write('P"+nn+"','"+j.ciudad+"' )")
        exec("worksheet.write('Q"+nn+"','"+j.contacto+"' )")
        exec("worksheet.write('R"+nn+"','"+str(j.por_ica)+"' )")
        exec("worksheet.write('S"+nn+"','"+str(j.por_ret_fte)+"' )")
        n += 1
    workbook.close()
    output.seek(0)
    filename = 'terceros.xlsx'
    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename="+filename
    
    return response    
    
