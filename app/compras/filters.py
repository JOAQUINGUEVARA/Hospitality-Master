
import django_filters
from django_filters import FilterSet,DateFromToRangeFilter,DateFilter,DateRangeFilter,DateTimeFromToRangeFilter
from django import forms
from .models import OrdenCompra,OrdenCompraDetalle,Despacho,DetalleDespacho,ProveedorItem
from compras.models import Proveedor 


class OrdenCompraFilter(django_filters.FilterSet):
    
    #fecha = DateRangeFilter()
    IdProveedor = django_filters.CharFilter(field_name='IdProveedor__razon_social',lookup_expr='icontains')
    numero = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = OrdenCompra
        fields = ['numero','fecha','IdProveedor','despacho']

class OrdenCompraFilter1(django_filters.FilterSet):
    
    #fecha = DateRangeFilter()
    #IdProveedor = django_filters.CharFilter(field_name='IdProveedor__identificacion',lookup_expr='icontains')
    numero = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = OrdenCompra
        fields = ['numero','IdProveedor']

class ProveedoresFilter(django_filters.FilterSet):
    
    identificacion = django_filters.CharFilter(lookup_expr='icontains')
    apenom = django_filters.CharFilter(lookup_expr='icontains')
    razon_social = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Proveedor
        fields = ['identificacion','IdTipoIdentificacion','razon_social','apenom','direccion','telefono','email',
                  'direccion','telefono','email','IdPais','departamento','ciudad','contacto','IdUsuario','por_ica','por_ret_fte','valor_debitos','valor_creditos',
                  'valor_saldo']
        
class ProveedoresNombreFilter(django_filters.FilterSet):
    
    apenom = django_filters.CharFilter(lookup_expr='icontains')
    razon_social = django_filters.CharFilter(lookup_expr='icontains')
    identificacion = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Proveedor
        fields = ['identificacion','razon_social','apenom']

class ProveedoresFilter1(django_filters.FilterSet):
    identificacion = django_filters.CharFilter(field_name='identificacion',lookup_expr='icontains')    
    apenom = django_filters.CharFilter(field_name='apenom',lookup_expr='icontains')
    razon_social = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Proveedor
        fields = ['identificacion','IdTipoIdentificacion','razon_social','apenom','direccion','telefono','email',
                  'direccion','telefono','email','IdPais','departamento','ciudad','contacto','IdUsuario','por_ica','por_ret_fte','valor_debitos','valor_creditos',
                  'valor_saldo']

class DespachoFilter(django_filters.FilterSet):
    
    #fecha = DateRangeFilter()
    IdProveedor = django_filters.CharFilter(field_name='IdProveedor__razon_social',lookup_expr='icontains')
    IdOrdenCompra = django_filters.CharFilter(field_name='IdOrdenCompra__mumero',lookup_expr='icontains')
    numero = django_filters.CharFilter(lookup_expr='icontains')        

    class Meta:
        model = Despacho
        fields = ['numero','fecha','IdOrdenCompra','IdProveedor']

class ProveedorItemFilter(django_filters.FilterSet):
    
    #fecha = DateRangeFilter()
    IdProveedor = django_filters.CharFilter(field_name='IdProveedor__razon_social',lookup_expr='icontains')
    IdItem = django_filters.CharFilter(field_name='IdItem__descripcion',lookup_expr='icontains')
    
    class Meta:
        model = ProveedorItem
        fields = ['IdProveedor','IdItem']