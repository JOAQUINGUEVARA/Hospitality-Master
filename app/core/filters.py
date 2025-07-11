from core.models import Tercero
import django_filters
from django_filters import FilterSet,DateFromToRangeFilter,DateFilter,DateRangeFilter,DateTimeFromToRangeFilter
from django import forms

class TerceroFilter(django_filters.FilterSet):
    
    identificacion = django_filters.CharFilter(lookup_expr='icontains')
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model =Tercero
        fields = ['identificacion','IdTipoIdentificacion','nombre1','nombre2','apel1','apel2','razon_social','nombre','direccion','telefono','email',
                  'direccion','telefono','email','IdPais','departamento','ciudad','contacto','IdUsuario','por_ica','por_ret_fte','valor_debitos','valor_creditos',
                  'valor_saldo']
        
class TerceroNombreFilter(django_filters.FilterSet):
    
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    identificacion = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model =Tercero
        fields = ['identificacion','nombre']
        
class TerceroFilter1(django_filters.FilterSet):
    identificacion = django_filters.CharFilter(field_name='identificacion',lookup_expr='icontains')    
    apenom = django_filters.CharFilter(field_name='apenom',lookup_expr='icontains')
    IdTipoTercero = django_filters.CharFilter(field_name='IdTipoTercero__descripcion',lookup_expr='icontains')

    class Meta:
        model = Tercero
        fields = ['identificacion','IdTipoIdentificacion','IdTipoTercero','nombre1','nombre2','apel1','apel2','razon_social','nombre','direccion','telefono','email',
                  'direccion','telefono','email','IdPais','departamento','ciudad','contacto','IdUsuario','por_ica','por_ret_fte','valor_debitos','valor_creditos',
                  'valor_saldo']