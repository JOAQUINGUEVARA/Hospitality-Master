from functools import partial
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import Ingrediente,Receta,RecetaIngrediente,OrdenProduccion
from inventarios.models import MaestroItem

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['producto',]

class RecetaIngredienteForm(forms.ModelForm):
    class Meta:
        model = RecetaIngrediente
        fields = ['ingrediente','cantidad_necesaria']

class OdenProduccionForm(forms.ModelForm):
    class Meta:
        model = OrdenProduccion
        fields = ['receta','cantidad_producir']

