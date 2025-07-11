from caja.models import ReciboCaja,PedidoCaja,PagoReciboCaja
import django_filters
from django_filters import FilterSet,DateFromToRangeFilter,DateFilter,DateRangeFilter,DateTimeFromToRangeFilter
from django import forms

class RecibosCajaFilter(django_filters.FilterSet):
    
    start_date = DateFilter(field_name='fecha',
                                           widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                           lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                         lookup_expr='lte', label='End Date')
    fecha = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    
    #fecha = DateRangeFilter()
    IdTercero = django_filters.CharFilter(field_name='IdTercero__apenom',lookup_expr='icontains')
    numero = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model =ReciboCaja
        fields = ['numero','fecha','IdTercero','IdCaja','IdHabitacion','IdSucursal','IdUsuario']
        
      
class PedidosCajaFilter(django_filters.FilterSet):
    
    start_date = DateFilter(field_name='fecha',
                                           widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                           lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                         lookup_expr='lte', label='End Date')
    fecha = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    numero = django_filters.CharFilter(lookup_expr='icontains')
    #IdMesa = django_filters.CharFilter(field_name='IdMesa__idMesa',lookup_expr='iexact')
    #IdHabitacion = django_filters.CharFilter(field_name='IdHabitacion__idHabitacion',lookup_expr='iexact')
    recibo_caja = django_filters.CharFilter(lookup_expr='icontains')
        
    class Meta:
        model =PedidoCaja
        fields = ['numero','fecha','IdTipoIngreso','IdCaja','IdMesa','IdHabitacion','recibo_caja','IdUsuario']

class PagosCajaFilter(django_filters.FilterSet):
    
    start_date = DateFilter(field_name='fecha',
                                           widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                           lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                         lookup_expr='lte', label='End Date')
    fecha = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    #fecha = DateRangeFilter()
    numero = django_filters.CharFilter(lookup_expr='icontains')
    IdTipoPago__iDTipoPago = django_filters.CharFilter(lookup_expr='icontains')
    IdTarjetaCredito__iDTarjetaCredito = django_filters.CharFilter(lookup_expr='icontains')
    recibo_caja = django_filters.CharFilter(lookup_expr='icontains')
    IdTercero = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model =PagoReciboCaja
        fields = ['numero','fecha','detalle','IdTipoPago','IdTercero','recibo_caja','IdTarjetaCredito','valor','IdSucursal','IdUsuario']


class PedidosCajaConsolidadoFilter(django_filters.FilterSet):
    
    start_date = DateFilter(field_name='fecha',
                                           widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                           lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                         lookup_expr='lte', label='End Date')
    fecha = DateFilter(field_name='fecha',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    #IdHabitacion = django_filters.CharFilter(field_name='IdHabitacion__idHabitacion',lookup_expr='iexact')
            
    class Meta:
        model =PedidoCaja
        fields = ['numero','fecha','IdTipoIngreso','IdCaja','IdHabitacion','IdMesa','recibo_caja','IdUsuario']        