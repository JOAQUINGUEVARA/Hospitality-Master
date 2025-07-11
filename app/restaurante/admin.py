from django.contrib import admin
from import_export import fields,resources
from import_export.admin import ImportExportModelAdmin

from restaurante.models import Mesa,ReservaMesa

class MesaResource(resources.ModelResource):
    class Meta:
        model = Mesa
        skip_unchanged = True
        report_skipped = True
        fields = ('idMesa','descripcion','numero_sillas','reserva')        
        exclude = ('id',)

@ admin.register (Mesa)
class Mesa(ImportExportModelAdmin):
    list_display= ('idMesa','descripcion','numero_sillas','reserva')
    search_fields = ['descripcion']

class ReservaMesaResource(resources.ModelResource):
    class Meta:
        model = ReservaMesa
        skip_unchanged = True
        report_skipped = True
        fields = ('IdMesa','descripcion','fecha_reserva','IdSucursal','IdUsuario')        
        exclude = ('id',)

@ admin.register (ReservaMesa)
class ReservaMesa(ImportExportModelAdmin):
    list_display= ('IdMesa','descripcion','fecha_reserva','IdSucursal','IdUsuario')
    search_fields = ['descripcion']    