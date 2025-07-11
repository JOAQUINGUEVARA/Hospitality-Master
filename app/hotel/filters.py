from hotel.models import ReservaHabitacion,RegistroHotel
import django_filters
from django_filters import FilterSet,DateFromToRangeFilter,DateFilter,DateRangeFilter,DateTimeFromToRangeFilter
from django import forms

class ReservasFilter(django_filters.FilterSet):
    nombre_reserva = django_filters.CharFilter(lookup_expr='icontains')

    fecha_ingreso = DateFilter(field_name='fecha_ingreso',
                                           widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                           lookup_expr='gte', label='Fecho Ingreso')
    fecha_salida = DateFilter(field_name='fecha_salida',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                         lookup_expr='lte', label='Fecha Salida')
   
    
    fecha_reserva = DateFilter(field_name='fecha_reserva',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = ReservaHabitacion
        fields = ['IdHabitacion','fecha_ingreso','fecha_salida','fecha_reserva']

class RegistrosFilter(django_filters.FilterSet):
    IdTercero = django_filters.CharFilter(field_name='IdTercero__apenom',lookup_expr='icontains')

    check_in = DateFilter(field_name='check_in',
                                           widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                           lookup_expr='gte', label='Fecho Ingreso')
    check_out = DateFilter(field_name='check_out',
                                         widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                                         lookup_expr='lte', label='Fecha Salida')
   
    class Meta:
        model = RegistroHotel
        fields = ['IdTercero','IdHabitacion','check_in','check_out']


