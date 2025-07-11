import django_filters
from django_filters import FilterSet,DateFromToRangeFilter,DateFilter,DateRangeFilter,DateTimeFromToRangeFilter
from django import forms
from .models import Receta,Ingrediente,OrdenProduccion


class RecetaFilter(django_filters.FilterSet):
    producto = django_filters.CharFilter(field_name='producto__descripcion',lookup_expr='icontains') 

    class Meta:
        model = Receta
        fields = ['producto']
        order_by = ['producto']

class IngredienteFilter(django_filters.FilterSet):
    descripcion= django_filters.CharFilter(lookup_expr='icontains')            
    
    class Meta:
        model = Ingrediente
        fields = ['descripcion']
        order_by = ['descripcion']        

class OrdenProduccionFilter(django_filters.FilterSet):
    #receta = django_filters.CharFilter(field_name='receta.producto__descripcion',lookup_expr='icontains')
    numero = django_filters.CharFilter(lookup_expr='icontains')         
    
    class Meta:
        model = OrdenProduccion
        fields = ['receta','numero']
        order_by = ['receta']