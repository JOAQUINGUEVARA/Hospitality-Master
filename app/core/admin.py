from django.contrib import admin
from import_export import fields,resources
from import_export.admin import ImportExportModelAdmin
from core.models import Pais,Departamento,Ciudad,TipoIdentificacion,Tercero,Sucursal,Empresa,ValorDefecto,Anio,Mes


admin.site.register(Empresa)


class PaisResource(resources.ModelResource):
    class Meta:
        model = Pais
        skip_unchanged = True
        report_skipped = True
        fields = ('idPais','descripcion')        
        exclude = ('id',)

@ admin.register (Pais)
class Pais(ImportExportModelAdmin):
    list_display= ('idPais','descripcion')
    search_fields = ['descripcion']
    list_per_page = 30

class DepartamentoResource(resources.ModelResource):
    class Meta:
        model = Departamento
        skip_unchanged = True
        report_skipped = True
        fields = ('idDepartamento','IdPais','descripcion')        
        exclude = ('id',)

@ admin.register (Departamento)
class Departamento(ImportExportModelAdmin):
    list_display= ('idDepartamento','IdPais','descripcion')
    search_fields = ['descripcion']
    list_per_page = 30

class CiudadResource(resources.ModelResource):
    class Meta:
        model = Ciudad
        skip_unchanged = True
        report_skipped = True
        fields = ('IdPais','IdDepartamento','idCiudad','descripcion')        
        exclude = ('id',)

@ admin.register (Ciudad)
class Ciudad(ImportExportModelAdmin):
    list_display= ('IdPais','IdDepartamento','idCiudad','descripcion')
    search_fields = ['descripcion']
    list_per_page = 30

class TipoIdentificacionResource(resources.ModelResource):
    class Meta:
        model = TipoIdentificacion
        skip_unchanged = True
        report_skipped = True
        fields = ('idTipoIdentificacion','descripcion')        
        exclude = ('id',)

@ admin.register (TipoIdentificacion)
class TipoIdentificacion(ImportExportModelAdmin):
    list_display= ('idTipoIdentificacion','descripcion')
    search_fields = ['descripcion']
    list_per_page = 30


class TerceroResource(resources.ModelResource):
    class Meta:
        model = Tercero
        skip_unchanged = True
        report_skipped = True
        fields = ('identificacion','IdTipoIdentificacion','nombre1','nombre2','apel1','apel2','apenom','razon_social','direccion','telefono',
                  'email','IdPais','departamento','ciudad','contacto','IdUsuario','por_ica','por_ret_fte','valor_debitos','valor_creditos','valor_saldo')        
        exclude = ('id',)

@ admin.register (Tercero)
class Tercero(ImportExportModelAdmin):
    list_display= ('identificacion','IdTipoIdentificacion','nombre1','nombre2','apel1','apel2','apenom','razon_social','direccion','telefono',
                  'email','IdPais','departamento','ciudad','contacto','IdUsuario','por_ica','por_ret_fte','valor_debitos','valor_creditos','valor_saldo')
    search_fields = ['identificacion','apenom','razon_social']
    list_per_page = 30

class SucursalResource(resources.ModelResource):
    class Meta:
        model = Sucursal
        skip_unchanged = True
        report_skipped = True
        fields = ('idSucursal','descripcion')        
        exclude = ('id',)

@ admin.register (Sucursal)
class Sucursal(ImportExportModelAdmin):
    list_display= ('idSucursal','descripcion')
    search_fields = ['descripcion']
    list_per_page = 30

class ValorDefectoResource(resources.ModelResource):
    class Meta:
        model = ValorDefecto
        skip_unchanged = True
        report_skipped = True
        fields = ('idValor','valor','descripcion')        
        exclude = ('id',)

@ admin.register (ValorDefecto)
class ValorDefecto(ImportExportModelAdmin):
    list_display= ('idValor','valor','descripcion')
    search_fields = ['descripcion']
    list_per_page = 30

class AnioResource(resources.ModelResource):
    class Meta:
        model = Anio
        skip_unchanged = True
        report_skipped = True
        fields = ('anio')        
        exclude = ('id',)

@ admin.register (Anio)
class Anio(ImportExportModelAdmin):
    list_display= ('anio',)
    search_fields = ['anio']
    list_per_page = 30

class MesResource(resources.ModelResource):
    class Meta:
        model = Mes
        skip_unchanged = True
        report_skipped = True
        fields = ('idMes','descripcion')        
        exclude = ('id',)

@ admin.register (Mes)
class Mes(ImportExportModelAdmin):
    list_display= ('idMes','descripcion')
    search_fields = ['descripcion']
    list_per_page = 30