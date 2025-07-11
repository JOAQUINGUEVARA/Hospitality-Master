
from django.contrib import admin
from import_export import fields,resources
from import_export.admin import ImportExportModelAdmin

from hotel.models import TipoHabitacion,Habitacion,ReservaHabitacion,RegistroHotel
#,RegistroHotel

class TipoHabitacionResource(resources.ModelResource):
    class Meta:
        model = TipoHabitacion
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipoHabitacion','descripcion')        
        exclude = ('id',)

@ admin.register (TipoHabitacion)
class TipoHabitacion(ImportExportModelAdmin):
    list_display= ('idTipoHabitacion','descripcion')
    search_fields = ['descripcion']
    list_per_page = 30

class HabitacionResource(resources.ModelResource):
    class Meta:
        model = Habitacion
        skip_unchanged = True
        report_skipped = True
        fields = ('idHabitacion','IdTipoHabitacion','descripcion','valor_noche','ocupada')        
        exclude = ('id',)

@ admin.register (Habitacion)
class Habitacion(ImportExportModelAdmin):
    list_display= ('idHabitacion','IdTipoHabitacion','descripcion','valor_noche','ocupada')
    search_fields = ['idHabitacion']
    list_per_page = 30


class ReservaHabitacionResource(resources.ModelResource):
    class Meta:
        model = ReservaHabitacion
        skip_unchanged = True
        report_skipped = True
        fields = ('consecutivo','IdHabitacion','descripcion','fecha_ingreso','fecha_salida','fecha_reserva','valor_reserva','nombre_reserva','telefono','email','pin','no_de_dias','no_de_noches')        
        exclude = ('id',)

@ admin.register (ReservaHabitacion)
class ReservaHabitacion(ImportExportModelAdmin):
    list_display= ('consecutivo','IdHabitacion','descripcion','fecha_ingreso','fecha_salida','fecha_reserva','valor_reserva','nombre_reserva','telefono','email','pin','no_de_dias','no_de_noches')
    search_fields = ['IdHabitacion']
    list_per_page = 30

class RegistroHotelResource(resources.ModelResource):
    class Meta:
        model = RegistroHotel
        skip_unchanged = True
        report_skipped = True
        fields = ('consecutivo','idHabitacion','IdTercero','descripcion','tarifa_habitacion','check_in','check_out','no_de_dias','no_de_noches','valor_pago',
                  'ocupacion','empresa','motivo_viaje','procedencia','destino','placa_vehiculo','dias_estadia','no_adultos','no_ninos','equipaje','pagado','no_recibo_caja')        
        exclude = ('id',)

@ admin.register (RegistroHotel)
class RegistroHotel (ImportExportModelAdmin):
    list_display= ('consecutivo','IdHabitacion','IdTercero','descripcion','tarifa_habitacion','check_in','check_out','no_de_dias','no_de_noches','valor_pago',
                  'ocupacion','empresa','motivo_viaje','procedencia','destino','placa_vehiculo','dias_estadia','no_adultos','no_ninos','equipaje','pagado','no_recibo_caja')
    search_fields = ['IdHabitacion','IdTercero.apenom']
    list_per_page = 20