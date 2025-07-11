from functools import partial
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from hotel.models import TipoHabitacion,Habitacion,ReservaHabitacion,RegistroHotel,AcompañanteHotel
from core.models import Tercero
from django.forms import formset_factory
from caja.forms import PagoReciboCaja

class TipoHabitacionForm(forms.ModelForm):
    class Meta:
        model = TipoHabitacion
        fields = ['idTipoHabitacion','descripcion']

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['idHabitacion','IdTipoHabitacion','descripcion','valor_noche','ocupada']        

class ReservaForm(forms.ModelForm):
    class Meta:
        model = ReservaHabitacion
        fields = ['IdHabitacion','descripcion','valor_reserva','nombre_reserva','telefono','email']
        widgets = {
            'fecha_ingreso': DatePickerInput(),
            'fecha_salida': DatePickerInput()
        }

class ValidaReservaForm(forms.ModelForm):
    class Meta:
        model = ReservaHabitacion
        fields = ['IdHabitacion','fecha_ingreso','fecha_salida']
        widgets = {
            'fecha_ingreso': DatePickerInput(),
            'fecha_salida': DatePickerInput()
        }

class RegistroForm(forms.ModelForm):
    class Meta:
        model = RegistroHotel
        fields = ['IdHabitacion','descripcion','tarifa_habitacion','check_in',
                  'ocupacion','empresa','motivo_viaje','procedencia','destino','placa_vehiculo','dias_estadia','no_adultos','no_ninos','equipaje',]        

        widgets = {
                'check_in': DatePickerInput(),
            }
class RegistroEditForm(forms.ModelForm):
    class Meta:
        model = RegistroHotel
        fields = ['IdHabitacion','descripcion','tarifa_habitacion','check_in',
                  'ocupacion','empresa','motivo_viaje','nacionalidad','procedencia','destino','placa_vehiculo','dias_estadia','no_adultos','no_ninos','equipaje',]        

        widgets = {
                'check_in': DatePickerInput(),
            }

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = RegistroHotel
        fields = ['check_out','descripcion']        

        widgets = {
                'check_out': DatePickerInput(),
            }
                
#RegistroFormSet = formset_factory(RegistroForm)

class TerceroRegistroHotelForm(forms.ModelForm):
    class Meta:
        model = Tercero
        fields = ['identificacion','IdTipoIdentificacion','identifica_de','nombre1','nombre2','apel1','apel2','razon_social','IdPais','departamento','ciudad',
                  'direccion','telefono','email','direccion','telefono','email','ocupacion',]
        
class PagoReciboCajaForm(forms.ModelForm):
    
    class Meta:
        model = PagoReciboCaja
        fields = ['IdTipoPago','IdTarjetaCredito','recibo_caja','detalle','valor'] 

class LiquidaEstadiaForm(forms.ModelForm):
    class Meta:
        model = RegistroHotel
        fields = ['IdHabitacion','descripcion','tarifa_habitacion','check_in','check_out','no_de_dias','no_de_noches',
                  'valor_pago',]        

        widgets = {
                'check_in': DatePickerInput(),
                'check_out': DatePickerInput(),
            }               

class AcompañanteHotelForm(forms.ModelForm):
    
    class Meta:
        model = AcompañanteHotel
        fields = ['identificacion','IdTipoIdentificacion','identifica_de','apenom','lugar_residencia']        
        
        
