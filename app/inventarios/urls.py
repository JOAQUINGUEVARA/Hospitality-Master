from django.urls import include, path
from caja import views as CajaViews
from inventarios import views as InventariosViews
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from profiles.urls import profiles_patterns
from registration.urls import registration_patterns
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views 

urlpatterns = [
    
    path('grupos_inventario_list/',InventariosViews.GruposInventarioListView,name='grupos_inventario_list'),
    path('crea_grupo_inventario/',InventariosViews.CreaGrupoInventarioView.as_view(),name='crea_grupo_inventario'),
    path('edita_grupo_inventario/<int:pk>/',InventariosViews.EditaGrupoInventarioView.as_view(),name='edita_grupo_inventario'),
    path('borra_grupo_inventario/<int:pk>/',InventariosViews.BorraGrupoInventarioView.as_view(),name='borra_grupo_inventario'),
    path('filtra_subgrupo_por_grupo/',InventariosViews.FiltraSubGrupoPorGrupoInventarioView,name='filtra_subgrupo_por_grupo'),
    path('sub_grupos_inventario_list/',InventariosViews.SubGruposInventarioListView,name='sub_grupos_inventario_list'),
    path('crea_sub_grupo_inventario/',InventariosViews.CreaSubGrupoInventarioView.as_view(),name='crea_sub_grupo_inventario'),
    path('edita_sub_grupo_inventario/<int:pk>/',InventariosViews.EditaSubGrupoInventarioView.as_view(),name='edita_sub_grupo_inventario'),
    path('borra_sub_grupo_inventario/<int:pk>/',InventariosViews.BorraSubGrupoInventarioView.as_view(),name='borra_sub_grupo_inventario'),

    path('bodegas_inventario_list/',InventariosViews.BodegasInventarioListView,name='bodegas_inventario_list'),
    path('crea_bodega_inventario/',InventariosViews.CreaBodegaInventarioView.as_view(),name='crea_bodega_inventario'),
    path('edita_bodega_inventario/<int:pk>/',InventariosViews.EditaBodegaInventarioView.as_view(),name='edita_bodega_inventario'),
    path('borra_bodega_inventario/<int:pk>/',InventariosViews.BorraBodegaInventarioView.as_view(),name='borra_bodega_inventario'),

    path('items_inventario_list/',InventariosViews.ItemsInventarioListView,name='items_inventario_list'),
    path('crea_item_inventario/',InventariosViews.CreaItemInventarioView.as_view(),name='crea_item_inventario'),
    path('edita_item_inventario/<int:pk>/',InventariosViews.EditaItemInventarioView.as_view(),name='edita_item_inventario'),
    path('borra_item_inventario/<int:pk>/',InventariosViews.BorraItemInventarioView.as_view(),name='borra_item_inventario'),
    path('detalle_item_inventario/<int:id>/',InventariosViews.DetalleItemInventarioView,name='detalle_item_inventario'),

    path('medidas_inventario_list/',InventariosViews.MedidasInventarioListView,name='medidas_inventario_list'),
    path('crea_medida_inventario/',InventariosViews.CreaMedidaInventarioView.as_view(),name='crea_medida_inventario'),
    path('edita_medida_inventario/<int:pk>/',InventariosViews.EditaMedidaInventarioView.as_view(),name='edita_medida_inventario'),
    path('borra_medida_inventario/<int:pk>/',InventariosViews.BorraMedidaInventarioView.as_view(),name='borra_medida_inventario'),

    path('acumulado_item_inventario_list/',InventariosViews.AcumuladoItemInventarioListView,name='acumulado_item_inventario_list'),
    path('entrada_acumulados_inventario/',InventariosViews.EntradaAcumuladosInventarioView,name='entrada_acumulados_inventario'),
    path('detalle_acumulado_item_inventario/<int:id>,<int:idbodega>/',InventariosViews.DetalleAcumuladoItemInventarioView,name='detalle_acumulado_item_inventario'),
    path('entrada_recupera_saldos_inventario',InventariosViews.EntradaRecuperacionSaldosInventarioView,name='entrada_recupera_saldos_inventario'),
    #path('entrada_recupera_saldos_inventario_uno/',InventariosViews.EntradaRecuperacionSaldosInventarioUnoView,name='entrada_recupera_saldos_inventario_uno'),
    path('recuperacion_saldos_inventario',InventariosViews.RecuperacionSaldosInventarioView,name='recuperacion_saldos_inventario'),
    path('recuperacion_saldos_inventario_uno/',InventariosViews.RecuperacionSaldosInventarioUnoView,name='recuperacion_saldos_inventario_uno'),

    path('direcciona_inventarios/<int:id>/',InventariosViews.DireccionaInventarios,name='direcciona_inventarios'),

    path('salidas_inventario_list/',InventariosViews.SalidasInventarioListView,name='salidas_inventario_list'),
    path('detalle_salida_inventario/<int:id>',InventariosViews.DetalleSalidaInventarioView,name='detalle_salida_inventario'),
    path('crea_salida_inventario/',InventariosViews.CreaSalidaInventarioView.as_view(),name='crea_salida_inventario'),
    path('verifica_detalle_salida_inventario/<int:id>/',InventariosViews.VerificaDetalleSalidaInventarioView,name='verifica_detalle_salida_inventario'),
    path('selecciona_item_salida_inventarios/<int:id>/',InventariosViews.SeleccionaItemSalidaInventariosView,name='selecciona_item_salida_inventarios'),
    path('filtra_item_salida_inventarios/',InventariosViews.FiltraItemSalidaInventariosView.as_view(),name='filtra_item_salida_inventarios'),
    path('crea_detalle_salida_inventario/<int:id>/',InventariosViews.CreaDetalleSalidaInventarioView,name='crea_detalle_salida_inventario'),
    path('edita_salida_inventario/<int:pk>/',InventariosViews.EditaSalidaInventarioView.as_view(),name='edita_salida_inventario'),
    path('valida_editar_salida_inventario/<int:id>/',InventariosViews.ValidaEditarSalidaInventarioView,name='valida_editar_salida_inventario'),
    path('valida_editar_detalle_salida_inventario/<int:id>/',InventariosViews.ValidaEditarDetalleSalidaInventarioView,name='valida_editar_detalle_salida_inventario'),
    path('valida_crea_detalle_salida_inventario/<int:id>/',InventariosViews.ValidaCreaDetalleSalidaInventarioView,name='valida_crea_detalle_salida_inventario'),
    path('edita_salida_detalle_inventario/<int:pk>/',InventariosViews.EditaDetalleSalidaInventarioView.as_view(),name='edita_salida_detalle_inventario'),
    path('borra_salida_inventario/<int:pk>/',InventariosViews.BorraSalidaInventarioView.as_view(),name='borra_salida_inventario'),
    path('borra_salida_detalle_inventario/<int:id>/',InventariosViews.BorraSalidaDetalleInventarioView,name='borra_salida_detalle_inventario'),
    path('borra_salida_venta_inventario/<int:id>/',InventariosViews.BorraSalidaPorVentaInventarioView,name='borra_salida_venta_inventario'),
    path('guarda_item_salida',InventariosViews.GuardaItemSalida,name='guarda_item_salida'),
    path('guarda_id_salida',InventariosViews.GuardaIdSalida,name='guarda_id_salida'),
    path('guarda_id_item_acumulado',InventariosViews.GuardaIdItemAcumulado,name='guarda_id_item_acumulado'),
    path('valida_borrar_salida_inventario/<int:id>/',InventariosViews.ValidaBorrarSalidaInventarioView,name='valida_borrar_salida_inventario'),
    path('valida_borrar_salida_detalle_inventario/<int:id>/',InventariosViews.ValidaBorrarDetalleSalidaInventarioView,name='valida_borrar_salida_detalle_inventario'),
    
    path('entradas_inventario_list/',InventariosViews.EntradasInventarioListView,name='entradas_inventario_list'),
    path('detalle_entrada_inventario/<int:id>',InventariosViews.DetalleEntradaInventarioView,name='detalle_entrada_inventario'),
    path('crea_entrada_inventario/',InventariosViews.CreaEntradaInventarioView.as_view(),name='crea_entrada_inventario'),
    path('edita_entrada_inventario/<int:id>/',InventariosViews.EditaEntradaInventarioView,name='edita_entrada_inventario'),
    path('edita_entrada_detalle_inventario/<int:pk>/',InventariosViews.EditaEntradaDetalleInventarioView.as_view(),name='edita_entrada_detalle_inventario'),
    path('borra_entrada_inventario/<int:pk>/',InventariosViews.BorraEntradaInventarioView.as_view(),name='borra_entrada_inventario'),
    path('borra_entrada_detalle_inventario/<int:id>/',InventariosViews.BorraEntradaDetalleInventarioView,name='borra_entrada_detalle_inventario'),
    path('verifica_detalle_entrada_inventario/<int:id>/',InventariosViews.VerificaDetalleEntradaInventarioView,name='verifica_detalle_entrada_inventario'),
    path('selecciona_item_entrada_inventarios/<int:id>/',InventariosViews.SeleccionaItemEntradaInventariosView,name='selecciona_item_entrada_inventarios'),
    path('filtra_item_entrada_inventarios/',InventariosViews.FiltraItemEntradaInventariosView.as_view(),name='filtra_item_entrada_inventarios'),
    path('guarda_item_entrada',InventariosViews.GuardaItemEntrada,name='guarda_item_entrada'),
    path('guarda_id_entrada',InventariosViews.GuardaIdEntrada,name='guarda_id_entrada'),
    path('guarda_id_detalle_entrada',InventariosViews.GuardaIdDetalleEntrada,name='guarda_id_detalle_entrada'),
    path('crea_detalle_entrada_inventario/<int:id>/',InventariosViews.CreaDetalleEntradaInventarioView,name='crea_detalle_entrada_inventario'),
    path('busca_item_inventario',InventariosViews.BuscaItemInventarioView,name='busca_item_inventario'),
    path('valida_editar_entrada_inventario/<int:id>/',InventariosViews.ValidaEditarEntradaInventarioView,name='valida_editar_entrada_inventario'),
    path('valida_editar_entrada_detalle_inventario/<int:id>/',InventariosViews.ValidaEditarDetalleEntradaInventarioView,name='valida_editar_entrada_detalle_inventario'),
    path('valida_borrar_entrada_inventario/<int:id>/',InventariosViews.ValidaBorrarEntradaInventarioView,name='valida_borrar_entrada_inventario'),
    path('valida_borrar_entrada_detalle_inventario/<int:id>/',InventariosViews.ValidaBorrarDetalleEntradaInventarioView,name='valida_borrar_entrada_detalle_inventario'),
    
    #path('mensaje_no_valor_entrada_inventario',InventariosViews.MensajeNoValorEntradaInventario,name='mensaje_no_valor_entrada_inventario'),
    
    path('entra_kardex/',InventariosViews.EntraKardexView,name='entra_kardex'),
    path('kardex/',InventariosViews.KardexView,name='kardex'),
    path('kardex_detalle/<int:id>/',InventariosViews.KardexDetalleView,name='kardex_detalle'),

    path('inventario_fisico/',InventariosViews.InventarioFisicoView,name='inventario_fisico'),
    path('entra_inventario_fisico/',InventariosViews.EntraInventarioFisicoView,name='entra_inventario_fisico'),
    path('crea_inventario_fisico/',InventariosViews.CreaInventarioFisicoView,name='crea_inventario_fisico'),
    path('edita_inventario_fisico/<int:pk>/',InventariosViews.EditaInventarioFisicoView.as_view(),name='edita_inventario_fisico'),
    path('ingreso_items_inventario_fisico/',InventariosViews.FiltraItemInventarioFisicoView.as_view(),name='ingreso_items_inventario_fisico'),
    path('item_inventario_fisico/',InventariosViews.ItemInventarioFisico,name='item_inventario_fisico'),
    path('Valida_borra_inventario_fisico/',InventariosViews.ValidaBorraInventarioFisicoView,name='valida_borra_inventario_fisico'),
    path('borra_inventario_fisico/',InventariosViews.BorraInventarioFisicoView,name='borra_inventario_fisico'),
    path('valida_ajuste_inventario_fisico/',InventariosViews.ValidaAjusteInventarioFisicoView,name='valida_ajuste_inventario_fisico'),
    
    path('crea_cierre_anual_inventario/',InventariosViews.CreaCierreAnualInventarioView,name='crea_cierre_anual_inventario'),
            
    #path('mensaje_proceso_terminado/',InventariosViews.MensajeProcesoTerminado,name='mensaje_proceso_terminado'),
    path('guarda_anio',InventariosViews.GuardaAnio,name='guarda_anio'),
    path('guarda_mes',InventariosViews.GuardaMes,name='guarda_mes'),
    path('guarda_bodega',InventariosViews.GuardaIdBodega,name='guarda_bodega'),
    #path('guarda_sucursal',InventariosViews.GuardaSucursal,name='guarda_sucursal'),

    path('ajax_bodegas',InventariosViews.AjaxBodegas,name='ajax_bodegas'),
    #path('ajax_sucursales',InventariosViews.AjaxSucursales,name='ajax_sucursales'),
    path('ajax_meses',InventariosViews.AjaxMeses,name='ajax_meses'),
    path('ajax_anios',InventariosViews.AjaxAnios,name='ajax_anios'),
    
    path('impresion_medidas_xls',InventariosViews.ImpresionMedidasXlsView,name='impresion_medidas_xls'),
    path('impresion_medidas',InventariosViews.ImpresionMedidasView,name='impresion_medidas'),

    
    path('impresion_bodegas_xls',InventariosViews.ImpresionBodegasXlsView,name='impresion_bodegas_xls'),
    path('impresion_bodegas',InventariosViews.ImpresionBodegasView,name='impresion_bodegas'),

    path('impresion_grupos_inventario_xls',InventariosViews.ImpresionGruposInventarioXlsView,name='impresion_grupos_inventario_xls'),
    path('impresion_grupos_inventario',InventariosViews.ImpresionGruposInventarioView,name='impresion_grupos_inventario'),
    path('impresion_subgrupos_inventario',InventariosViews.ImpresionSubGruposInventarioView,name='impresion_subgrupos_inventario'),
    path('impresion_subgrupos_inventario_xls',InventariosViews.ImpresionSubGruposInventarioXlsView,name='impresion_subgrupos_inventario_xls'),
    path('impresion_items_inventario_xls',InventariosViews.ImpresionItemsInventarioXlsView,name='impresion_items_inventario_xls'),
    #path('impresion_items_inventario',InventariosViews.ImpresionItemsInventarioView,name='impresion_items_inventario'),
    path('impresion_acumulados_inventario',InventariosViews.ImpresionAcumuladosInventarioView,name='impresion_acumulados_inventario'),
    path('impresion_acumulados_inventario_un_item/<int:iditem>/',InventariosViews.ImpresionAcumuladosInventarioUnItemView,name='impresion_acumulados_inventario_un_item'),
    path('impresion_acumulados_inventario_xls',InventariosViews.ImpresionAcumuladosInventarioXlsView,name='impresion_acumulados_inventario_xls'),
    path('impresion_acumulados_inventario_un_item_xls/<int:iditem>/',InventariosViews.ImpresionAcumuladosInventarioXlsUnItemView,name='impresion_acumulados_inventario_un_item_xls'),
    path('impresion_kardex_inventario',InventariosViews.ImpresionKardexInventarioView,name='impresion_kardex_inventario'),
    path('impresion_kardex_inventario_xls',InventariosViews.ImpresionKardexInventarioXlsView,name='impresion_kardex_inventario_xls'),
    path('impresion_entradas_inventario',InventariosViews.ImpresionEntradasInventarioView,name='impresion_entradas_inventario'),
    path('impresion_entradas_inventario_xls',InventariosViews.ImpresionEntradasInventarioXlsView,name='impresion_entradas_inventario_xls'),
    path('impresion_salidas_inventario',InventariosViews.ImpresionSalidasInventarioView,name='impresion_salidas_inventario'),
    path('impresion_salidas_inventario_xls',InventariosViews.ImpresionSalidasInventarioXlsView,name='impresion_salidas_inventario_xls'),
    path('impresion_inventario_fisico_xls',InventariosViews.ImpresionInventarioFisicoXlsView,name='impresion_inventario_fisico_xls'),
    path('impresion_inventario_fisico',InventariosViews.ImpresionInventarioFisicoView,name='impresion_inventario_fisico'),
    
    path('impresion_items_grupos_subgrupos/', InventariosViews.ImpresionItemsInventarioGrupoSubgruposView, name='impresion_items_grupos_subgrupos'),
    path('impresion_items_precios/', InventariosViews.ImpresionItemsPreciosView, name='impresion_items_precios'),
    path('impresion_items_punto_compra/', InventariosViews.ImpresionItemsPuntoCompraView, name='impresion_items_punto_compra'),
    path('impresion_items_alfabetico/', InventariosViews.ImpresionItemsAlfabeticoView, name='impresion_items_alfabetico'),
    
    path('impresion_items_grupos_subgrupos_xls/', InventariosViews.ImpresionItemsInventarioGrupoSubgruposXlsView, name='impresion_items_grupos_subgrupos_xls'),
    path('impresion_items_precios_xls/', InventariosViews.ImpresionItemsPreciosXlsView, name='impresion_items_precios_xls'),
    path('impresion_items_punto_compra_xls/', InventariosViews.ImpresionItemsPuntoCompraXlsView, name='impresion_items_punto_compra_xls'),
    path('impresion_items_alfabetico_xls/', InventariosViews.ImpresionItemsAlfabeticoXlsView, name='impresion_items_alfabetico_xls'),

    path('menu_procesos_inventario',InventariosViews.MenuProcesosInventario.as_view(), name='menu_procesos_inventario'),
    path('pone_anio_inventarios',InventariosViews.PoneAnioInventariosView,name='pone_anio_inventarios'),
    path('entra_cierre_anual_inventario/',InventariosViews.EntraCierreAnualInventarioView,name='entra_cierre_anual_inventario'),
    path('valida_traslado_bodegas_grupos_item',InventariosViews. ValidaTrasladoBodegasGruposItemsview,name='valida_traslado_bodegas_grupos_item'),
    path('traslado_bodegas_grupos_item',InventariosViews.TrasladoBodegasGruposItemView,name='traslado_bodegas_grupos_item'),
    path('cierre_anual_inventario/',InventariosViews.CierreAnualInventarioView,name='cierre_anual_inventario'),
    path('crea_ajuste_inventario_fisico/',InventariosViews.CreaAjusteInventarioFisicoView.as_view(),name='crea_ajuste_inventario_fisico'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Sitio Administrativo Hospitality - Plus'    
