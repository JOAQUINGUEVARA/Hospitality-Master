from django.urls import include, path,include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from cocina import views as cocinaViews 

urlpatterns = [
    
    #path('menu_cocina',cocinaViews.MenuCocinaView, name='nmenu_cocina'),
    #path('ingredientes_lista/',cocinaViews.IngredienteListView,name='ingredientes_lista'),
    path('recetas_lista/',cocinaViews.RecetaListView,name='recetas_lista'),
    path('receta_ingredientes_lista/<int:id>',cocinaViews.RecetaIngredientesListView,name='receta_ingredientes_lista'),
    path('crea_receta/',cocinaViews.CreaRecetaView.as_view(),name='crea_receta'),
    #path('edita_receta/<int:id>',cocinaViews.EditaRecetaView,name='edita_receta'),
    path('borra_receta/<int:pk>',cocinaViews.BorraRecetaView.as_view(),name='borra_receta'),
    path('impresion_recetas_xls',cocinaViews.ImpresionRecetasXlsView,name='impresion_recetas_xls'),
    path('impresion_recetas',cocinaViews.ImpresionRecetasView,name='impresion_recetas'),
    path('filtrar_item_inventario_materia_prima',cocinaViews.FiltrarItemInventarioMateriaPrimaView,name='filtrar_item_inventario_materia_prima'),
    path('ingredientes_lista/',cocinaViews.IngredienteListView,name='ingredientes_lista'),
    path('receta_ingrediente/<int:id>/',cocinaViews.RecetaIngredienteView,name='receta_ingrediente'),
    #path('busca_receta_ingrediente/<int:id>',cocinaViews.BuscaRecetaIngredienteView.as_view(),name='busca_receta_ingredientes'), 
    path('crea_ingrediente_receta/<int:pk>/',cocinaViews.CreaIngredienteRecetaView.as_view(),name='crea_ingrediente_receta'),
    path('edita_ingrediente_receta/<int:pk>/',cocinaViews.EditaIngredienteRecetaView.as_view(),name='edita_ingrediente_receta'),
    path('borra_ingrediente_receta/<int:pk>/',cocinaViews.BorraIngredienteRecetaView.as_view(),name='borra_ingrediente_receta'),
    path('guarda_id_receta',cocinaViews.GuardaIdReceta,name='guarda_id_receta'),
    path('guarda_id_producto',cocinaViews.GuardaIdProducto,name='guarda_id_producto'),
    path('guarda_id_ingrediente_receta',cocinaViews.GuardaIdIngredienteReceta,name='guarda_id_ingrediente_receta'),
    path('crea_ingrediente_receta<int:id>/',cocinaViews.CreaIngredienteRecetaView.as_view(),name='crea_ingrediente_receta'),
    #path('obtener_unidad_medida',cocinaViews.ObtenerUnidadMedidaView,name='obtener_unidad_medida'),
    path('procesos_cocina/',cocinaViews.MenuProcesosCocinaView.as_view(),name='procesos_cocina'),
    path('ordenes_produccion_lista/',cocinaViews.OrdenProduccionListView,name='ordenes_produccion_lista'),    
    path('crea_orden_produccion/',cocinaViews.CreaOrdenProduccionView.as_view(),name='crea_orden_produccion'),
    path('valida_borra_orden_produccion/<int:id>/',cocinaViews.ValidaBorraOrdenProduccionView,name='borra_orden_produccion'),
    path('borra_orden_produccion/<int:id>/',cocinaViews.BorraOrdenProduccionView.as_view(),name='valida_borra_orden_produccion'),
    path('valida_edita_orden_produccion/<int:id>/',cocinaViews.ValidaEditaOrdenProduccionView,name='valida_edita_orden_produccion'),
    path('edita_orden_produccion/<int:pk>/',cocinaViews.EditaOrdenProduccionView.as_view(),name='edita_orden_produccion'),
    path('impresion_ordenes_produccion_xls',cocinaViews.ImpresionOrdenesProduccionXlsView,name='impresion_ordenes_produccion_xls'),
    path('impresion_ordenes_produccion',cocinaViews.ImpresionOrdenesProduccionView,name='impresion_ordenes_produccion'),
    path('carga_items_orden_produccion/<int:id>/',cocinaViews.CargaItemsOrdenProduccionView,name='carga_items_orden_produccion'),
    path('valida_carga_items_orden_produccion/<int:id>/',cocinaViews.ValidaCargaItemsOrdenProduccionView,name='valida_carga_items_orden_produccion'),
    path('orden_produccion_detalle/<int:id>/',cocinaViews.OrdenProduccionDetalleView,name='orden_produccion_detalle'),
    path('guarda_id_orden_produccion',cocinaViews.GuardaIdOrdenProduccion,name='guarda_id_orden_produccion'),
    path('ejecuta_orden_produccion/<int:id>/',cocinaViews.EjecutaOrdenProduccionView,name='ejecuta_orden_produccion'),
    path('aplica_orden_produccion/<int:id>/',cocinaViews.AplicaOrdenProduccionView,name='aplica_orden_produccion'),
    path('valida_borrado_ingrediente_orden_produccion/<int:id>/',cocinaViews.ValidaBorradoIngredienteOrdenProduccionView,name='valida_borrado_ingrediente_orden_produccion'),
    path('pone_ingrediente', cocinaViews.PoneIngredienteView, name='pone_ingrediente'),
    path('menu_procesos_cocina/', cocinaViews.MenuProcesosCocinaView.as_view(), name='menu_procesos_cocina'),
    
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Sitio Administrativo Hospitality - Plus'    