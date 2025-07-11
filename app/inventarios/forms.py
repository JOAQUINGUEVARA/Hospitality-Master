from functools import partial
#from bootstrap_modal_forms.forms import BSModalModelForm
#from solicitudes.models import Solicitud,SolicitudDetalle,PrecioInjerto
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from inventarios.models import Grupo,SubGrupo,Bodega,MaestroItem,Medida,AcumuladoItem,Salida,SalidaDetalle,Entrada,EntradaDetalle,InventarioFisico,AjusteInventarioFisico
from core.models import Mes,Anio,Sucursal


class GruposInventariosForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['descripcion','IdBodega']

class SubGruposInventariosForm(forms.ModelForm):
    class Meta:
        model = SubGrupo
        fields = ['IdGrupo','descripcion']

class BodegasInventariosForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ["idBodega","descripcion","direccion","telefonos","responsable"]

class ItemsInventariosForm(forms.ModelForm):
    class Meta:
        model = MaestroItem
        fields = ["IdGrupo","IdSubGrupo","descripcion","IdUnidadMedida","marca","referencia_fabrica","valor_venta","valor_compra","tipo_producto","por_iva","IdBodega",
              "cant_maxima","cant_minima","costo_prom","acumula","estadia"]
    valor_venta = forms.DecimalField(max_digits=4, decimal_places=2, localize=True)

class MedidasInventariosForm(forms.ModelForm):
    class Meta:
        model = Medida
        fields = ['descripcion']


class AcumuladoItemsInventariosForm(forms.ModelForm):
    class Meta:
        model = AcumuladoItem
        fields = ['IdItem','IdBodega']

class SalidasInventariosForm(forms.ModelForm):
    class Meta:
        model = Salida
        fields = ['fecha','detalle']
        widgets = {
            'fecha': DatePickerInput()
        }

class SalidasInventariosDetalleForm(forms.ModelForm):
    class Meta:
        model = SalidaDetalle
        fields = ['numero','IdItem','IdBodega','valor','cantidad','valor_total']

class EntradasInventariosForm(forms.ModelForm):
    class Meta:
        model = Entrada
        #fields = ['fecha','IdTipoDocumento','detalle','IdProveedor','factura_compra','orden_compra']
        fields = ['fecha','IdTipoDocumento','detalle']
        widgets = {
            'fecha': DatePickerInput()
        }

class EntradasInventariosDetalleForm(forms.ModelForm):
    class Meta:
        model = EntradaDetalle
        fields = ['IdItem','IdBodega','valor','cantidad','valor_total']

class InventarioFisicoForm(forms.ModelForm):
    class Meta:
        model = InventarioFisico
        fields = ['inv_fis']

class AjusteInventariosForm(forms.ModelForm):
    class Meta:
        model = AjusteInventarioFisico
        fields = ['fecha','IdAnio','IdMes','IdBodega']
        widgets = {
            'fecha': DatePickerInput()
        }        

class MesForm(forms.ModelForm):
    class Meta:
        model = Mes
        fields = ['descripcion']

class AnioForm(forms.ModelForm):
    class Meta:
        model = Anio
        fields = ['anio']

class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ['descripcion'] 

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['descripcion']