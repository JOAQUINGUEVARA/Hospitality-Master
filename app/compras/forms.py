from functools import partial
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Proveedor,OrdenCompra,OrdenCompraDetalle,Despacho,DetalleDespacho
from .models import EmpaqueItem

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['identificacion','IdTipoIdentificacion','nombre1','nombre2','apel1','apel2','razon_social','direccion','telefono','email',
                  'IdPais','departamento','ciudad','contacto','por_ica','por_ret_fte']
        
class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = OrdenCompra
        fields = ['fecha','detalle','IdProveedor','IdSucursal']

    fecha = forms.DateField(widget=DatePickerInput())


class OrdenCompraDetalleForm(forms.ModelForm):
    class Meta:
        model = OrdenCompraDetalle
        fields = ['IdItem','cantidad_empaque','cantidad_unidad_empaque','valor_unidad_empaque','cantidad_unidades_compra','valor_compra']

class ProveedorOrdenCompraForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['identificacion','IdTipoIdentificacion','nombre1','nombre2','apel1','apel2','razon_social','IdPais','departamento','ciudad',
                  'direccion','telefono','email','contacto']
        
class DespachoForm(forms.ModelForm):
    class Meta:
        model = Despacho
        fields = ['fecha','detalle','IdOrdenCompra','IdProveedor','IdSucursal']

    fecha = forms.DateField(widget=DatePickerInput()) 

class DetalleDespachoForm(forms.ModelForm):
    class Meta:
        model = DetalleDespacho
        fields = ['cantidad_enviada']

class ItemEmpaqueForm(forms.ModelForm):
    class Meta:
        model = EmpaqueItem
        fields = ['descripcion','cantidad']

   