import django_filters
from django_filters import FilterSet,DateFromToRangeFilter,DateFilter,DateRangeFilter,DateTimeFromToRangeFilter
from django import forms
from inventarios.models import MaestroItem,AcumuladoItem,Salida,SalidaDetalle,Entrada,EntradaDetalle,Kardex,InventarioFisico,SubGrupo

class SubGrupoFilter(django_filters.FilterSet):
    #IdGrupo = django_filters.CharFilter(field_name='IdGrupo__descripcion',lookup_expr='icontains')    
    class Meta:
        model = SubGrupo 
        fields = ['IdGrupo','descripcion']
        
class MaestroItemsFilter(django_filters.FilterSet):
    #ini_item = django_filters.CharFilter(field_name='idItem',lookup_expr='gte', label='Start Item')
    #fin_item = django_filters.CharFilter(field_name='idItem',lookup_expr='lte', label='End Date')
    descripcion= django_filters.CharFilter(lookup_expr='icontains')            
    class Meta:
        model = MaestroItem
        fields = ['IdGrupo','IdSubGrupo','descripcion']


class MaestroItemsFilter1(django_filters.FilterSet):
    #idItem = django_filters.CharFilter(field_name='IdItem__descripcion',lookup_expr='icontains')
    #ini_item = django_filters.CharFilter(field_name='idItem',lookup_expr='gt', label='Start Item')
    #fin_item = django_filters.CharFilter(field_name='idItem',lookup_expr='lt', label='End Date')
    descripcion= django_filters.CharFilter(lookup_expr='icontains')                
    
    class Meta:
        model =MaestroItem
        fields = ['IdGrupo','IdSubGrupo']


class AcumuladoItemsInventarioFilter(django_filters.FilterSet):
    IdItem = django_filters.CharFilter(field_name='IdItem__descripcion',lookup_expr='icontains')    
    #IdSucursal = django_filters.CharFilter(field_name='IdSucursal__descripcion',lookup_expr='icontains')
    #IdBodega = django_filters.CharFilter(field_name='IdBodega__descripcion',lookup_expr='icontains')
    
    class Meta:
        model = AcumuladoItem
        fields = ['IdItem','IdBodega']

class SalidasInventarioFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name='fecha',
                                           widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                           lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                         lookup_expr='lte', label='End Date')
    fecha = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    numero = django_filters.CharFilter(lookup_expr='icontains')
    #IdSucursal = django_filters.CharFilter(field_name='IdSucursal__descripcion',lookup_expr='icontains')
    IdBodega = django_filters.CharFilter(field_name='IdBodega__descripcion',lookup_expr='icontains')
    #IdTipoDocumento = django_filters.CharFilter(field_name='IdTipoDocumento__descripcion',lookup_expr='icontains')
    pedido_caja = django_filters.CharFilter(field_name='pedido_caja',lookup_expr='icontains')
        
    class Meta:
        model = Salida
        fields = ['fecha','numero','pedido_caja','IdTipoDocumento','IdSucursal','IdBodega']

class EntradasInventarioFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name='fecha',
                                           widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                           lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                         lookup_expr='lte', label='End Date')
    fecha = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    numero = django_filters.CharFilter(lookup_expr='icontains')
    #IdSucursal = django_filters.CharFilter(field_name='IdSucursal__descripcion',lookup_expr='icontains')
    IdBodega = django_filters.CharFilter(field_name='IdBodega__descripcion',lookup_expr='icontains')
    #IdTipoDocumento = django_filters.CharFilter(field_name='IdTipoDocumento__descripcion',lookup_expr='icontains')
    despacho = django_filters.CharFilter(field_name='despacho',lookup_expr='icontains')

    class Meta:
        model = Entrada
        fields = ['fecha','numero','IdTipoDocumento','factura_compra','orden_compra','IdSucursal','IdBodega']


class InventarioFisicoFilter(django_filters.FilterSet):
    
    descripcion = django_filters.CharFilter(field_name='IdItem__descripcion',lookup_expr='icontains')    
    IdBodega = django_filters.CharFilter(field_name='IdBodega__descripcion',lookup_expr='icontains')
    #IdSucursal = django_filters.CharFilter(field_name='IdSucursal__descripcion',lookup_expr='icontains')
    
    class Meta:
        model = InventarioFisico
        fields = ['IdItem'] 

    