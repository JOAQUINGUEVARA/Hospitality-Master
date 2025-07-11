from django.forms import DateTimeField
from django.utils import timezone
from datetime import date
from functools import partial
#from bootstrap_modal_forms.forms import BSModalModelForm
from core.models import Tercero
from django import forms


class TerceroForm(forms.ModelForm):
    class Meta:
        model = Tercero
        fields = ['identificacion','IdTipoIdentificacion','identifica_de','nombre1','nombre2','apel1','apel2','razon_social','nombre','direccion','telefono','email','ocupacion',
                  'IdPais','departamento','ciudad','contacto','por_ica','por_ret_fte']
        
  
class TerceroReciboCajaForm(forms.ModelForm):
    class Meta:
        model = Tercero
        fields = ['identificacion','IdTipoIdentificacion','identifica_de','nombre1','nombre2','apel1','apel2','razon_social','IdPais','departamento','ciudad',
                  'direccion','telefono','email','direccion','telefono','email']