from django.forms import DateTimeField
from django.utils import timezone
from datetime import date
from functools import partial
#from bootstrap_modal_forms.forms import BSModalModelForm
#from solicitudes.models import Solicitud,SolicitudDetalle,PrecioInjerto
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from caja.models import ReciboCaja,ReciboCajaDetalle,SesionCaja,PedidoCaja,PedidoCajaDetalle,PagoReciboCaja


class ReciboCajaForm(forms.ModelForm):
    class Meta:
        model = ReciboCaja
        fields = ['fecha','IdTercero']

    fecha = forms.DateField(widget=DatePickerInput())

class ReciboCajaManualForm(forms.ModelForm):
    class Meta:
        model = ReciboCaja
        fields = ['fecha','detalle','IdTercero','IdCaja','valor']

    fecha = forms.DateField(widget=DatePickerInput())

class ReciboCajaDetalleForm(forms.ModelForm):
    class Meta:
        model = ReciboCajaDetalle
        fields = ['IdItem','cantidad','valor','valor_total']

class SesionCajaForm(forms.ModelForm):
    
    class Meta:
        model = SesionCaja
        fields = ['IdCaja']
        #widgets = {'IdSucursal': forms.HiddenInput(),'IdUsuario': forms.HiddenInput()}            

class PedidoCajaForm(forms.ModelForm):
    
    class Meta:
        model = PedidoCaja
        fields = ['fecha','IdCaja','IdMesa','IdHabitacion']

    fecha = forms.DateField(widget=DatePickerInput())

class PedidoCajaDetalleForm(forms.ModelForm):
    class Meta:
        model = PedidoCajaDetalle
        fields = ['IdItem','cantidad','valor']     

class PagoReciboCajaForm(forms.ModelForm):
    
    class Meta:
        model = PagoReciboCaja
        fields = ['IdTipoPago','IdTarjetaCredito','recibo_caja','detalle','valor']

