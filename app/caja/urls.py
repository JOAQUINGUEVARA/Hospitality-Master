from caja import views as CajaViews
from django.contrib import admin
from django.conf.urls import *
from django.contrib import admin
#from django.urls import path
#from core.views import HomePageView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
#from accounts.urls import registration_patterns
#from messenger.urls import messenger_patterns
from profiles.urls import profiles_patterns
from registration.urls import registration_patterns
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('apertura_caja',CajaViews.AperturaCajaView,name='apertura_caja'),
    path('ingreso_caja/<int:id>/',CajaViews.IngresoCajaView,name='ingreso_caja'),

    path('cierre_caja/<int:id>/',CajaViews.CierreCajaView,name='cierre_caja'),
    path('acepta_cierre_caja',CajaViews.AceptaCierreCajaView,name='acepta_cierre_caja'),
    path('niega_cierre_caja',CajaViews.NiegaCierreCajaView,name='niega_cierre_caja'),

    #path('selecciona_cargo_pedido_caja',CajaViews.SeleccionaCargoPedidoCajaView,name='selecciona_cargo_pedido_caja'),
    path('crea_pedido_caja_mesa/<int:id>/',CajaViews.CreaPedidoCajaMesaView,name='crea_pedido_caja_mesa'),
    path('crea_pedido_caja_habitacion/<int:id>/',CajaViews.CreaPedidoCajaHabitacionView,name='crea_pedido_caja_habitacion'),
    path('edita_pedido_caja/<int:pk>/',CajaViews.EditaPedidoCajaView.as_view(),name='edita_pedido_caja'),
    path('direcciona_recibo_caja/',CajaViews.DireccionaReciboCajaView,name='direcciona_recibo_caja'),
    path('direcciona_recibo_caja_detalle/',CajaViews.DireccionaReciboCajaDetalleView,name='direcciona_recibo_caja_detalle'),
    #path('direcciona_caja_pedido_detalle/',CajaViews.DireccionaCajaDesdePedidoDetalleView,name='direcciona_caja_pedido_detalle'),
    #path('direcciona_caja_desde_pagos',CajaViews.DireccionaCajaDesdePagosView,name='direcciona_caja_desde_pagos'),
    path('direcciona_pedido/',CajaViews.DireccionaPedidoView,name='direcciona_pedido'),
    path('direcciona_pedido_detalle/',CajaViews.DireccionaPedidoDetalleView,name='direcciona_pedido_detalle'),
    path('valida_borrado_pedido_caja/<int:id>/',CajaViews.ValidaBorradoPedidoCajaView,name='valida_borrado_pedido_caja'),
    path('valida_borrado_item_pedido_caja/<int:id>/',CajaViews.ValidaBorradoItemPedidoCajaView,name='valida_borrado_item_pedido_caja'),
    path('valida_borrado_detalle_pedido_caja/<int:id>/',CajaViews.ValidaBorradoDetallePedidoCajaView,name='valida_borrado_detalle_pedido_caja'),
    path('valida_edita_item_pedido_caja/<int:id>/',CajaViews.ValidaEditaItemPedidoCajaView,name='valida_edita_item_pedido_caja'),
    path('borra_item_pedido_caja/<int:id>/',CajaViews.BorraItemPedidoCajaView,name='borra_item_pedido_caja'),
    path('borra_pedido_caja/<int:id>/',CajaViews.BorraPedidoCajaView,name='borra_pedido_caja'),
    path('selecciona_item_pedido_caja/<int:id>/',CajaViews.SeleccionaItemPedidoCajaView,name='selecciona_item_pedido_caja'),
    path('filtra_item_pedido_caja/',CajaViews.FiltraItemPedidoCajaView.as_view(),name='filtra_item_pedido_caja'),
    path('item_pedido_caja',CajaViews.ItemPedidoCaja,name='item_pedido_caja'),
    path('detalle_pedido_caja/<int:id>/',CajaViews.PedidoCajaDetalleListaView,name='detalle_pedido_caja'),
    path('edita_detalle_pedido_caja/<int:id>/',CajaViews.EditaDetallePedidoCajaView,name='edita_detalle_pedido_caja'),
    #path('confirma_cierre_pedido_caja/<int:id>/',CajaViews.ConfirmaCierrePedidoCajaView,name='confirma_cierre_pedido_caja'),
    path('valida_cierre_pedido_caja/<int:id>/',CajaViews.ValidaCierrePedidoCajaView,name='valida_cierre_pedido_caja'),
    path('cierre_pedido_caja',CajaViews.CierrePedidoCajaView,name='cierre_pedido_caja'),
    path('crea_recibo_caja',CajaViews.CreaReciboCajaView,name='crea_recibo_caja'),
    path('busca_tercero_cierre_pedido_caja',CajaViews.BuscaTerceroCierrePedidoCajaView.as_view(),name='busca_tercero_cierre_pedido_caja'),
    path('crea_tercero_cierre_pedido_caja/<int:id>/',CajaViews.CreaTerceroCierrePedidoCajaView.as_view(),name='crea_tercero_cierre_pedido_caja'),
    #path('tercero_cierre_pedido_caja/',CajaViews.TerceroCierrePedidoCajaView.as_view(),name='tercero_cierre_pedido_caja'),
    path('guarda_id_pedido_caja/',CajaViews.GuardaIdPedidoCajaView,name='guarda_id_pedido_caja'),
    path('guarda_id_habitacion/',CajaViews.GuardaIdHabitacionView,name='guarda_id_habitacion'),
    #path('ingreso_items_pedido_caja/<int:id>/',CajaViews.IngresoItemsPedidoCajaView.as_view(),name='ingreso_items_pedido_caja'),
    #path('ingreso_items_pedido_caja_detalle/<int:id>/',CajaViews.IngresoItemsPedidoCajaDetalleView.as_view(),name='ingreso_items_pedido_caja_detalle'),
    #path('crea_item_pedido_caja/<int:id>/',CajaViews.CreaItemPedidoCajaView,name='crea_item_pedido_caja'),
    path('pedido_caja_lista_todos/',CajaViews.PedidoCajaListaTodosView,name='pedido_caja_lista_todos'),
    path('pedido_caja_lista/',CajaViews.PedidoCajaListaView,name='pedido_caja_lista'),
    path('selecciona_tercero_pedido_caja',CajaViews.SeleccionaTerceroPedidoCaja,name='selecciona_tercero_pedido_caja'),
    path('guarda_id_pedido_caja/',CajaViews.GuardaIdPedidoCaja,name='guarda_id_pedido_caja'),
    #path('crea_recibo_caja_lista',CajaViews.CreaReciboCajaView,name='crea_recibo_caja'),
    path('sube_terceros',CajaViews.SubeTerceros,name='sube_terceros'),
    path('recibo_caja_lista/',CajaViews.ReciboCajaListaView,name='recibo_caja_lista'),
    path('recibo_caja_lista_todos/',CajaViews.ReciboCajaListaTodosView,name='recibo_caja_lista_todos'),
    path('recibo_caja_detalle/<int:id>/',CajaViews.ReciboCajaDetalleListaView,name='recibo_caja_detalle'),
    path('pago_recibo_caja/<int:id>/',CajaViews.PagoReciboCajaView.as_view(),name='pago_recibo_caja'),
    #path('direcciona_pago_recibo_caja',CajaViews.PagoReciboCajaView.as_view(),name='direcciona_pago_recibo_caja'),
    path('mensaje_recibo_caja_pagado/',CajaViews.MensajeReciboCajaPagadoView,name='mensaje_recibo_caja_pagado'),
    path('direcciona_pago_caja',CajaViews.DireccionaPagoCaja,name='direcciona_pago_caja'),
    path('guarda_id_recibo_caja',CajaViews.GuardaIdReciboCaja,name='guarda_id_recibo_caja'),
    path('pagos_caja_lista/',CajaViews.PagosCajaListaView,name='pagos_caja_lista'),
    path('pagos_caja_lista_todos/',CajaViews.PagosCajaListaTodosView,name='pagos_caja_lista_todos'),
    path('pagos_caja_lista_consolidado/',CajaViews.PagosCajaListaConsolidadoView,name='pagos_caja_lista_consolidado'),
    path('cierre_pedido_caja_consolidado',CajaViews.CierrePedidoCajaConsolidadoView,name='cierre_pedido_caja_consolidado'),
    path('busca_tercero_cierre_pedido_caja_consolidado',CajaViews.BuscaTerceroCierrePedidoCajaConsolidadoView.as_view(),name='busca_tercero_cierre_pedido_caja_consolidado'),
    path('selecciona_caja_recibo_caja_consolidado',CajaViews.SeleccionaCajaReciboCajaConsolidadoView.as_view(),name='selecciona_caja_recibo_caja_consolidado'),
    path('recibo_caja_consolidado/<int:id>/',CajaViews.ReciboCajaConsolidadoView,name='recibo_caja_consolidado'),
    path('crea_recibo_caja_consolidado/<int:id>/',CajaViews.CreaReciboCajaConsolidadoView,name='crea_recibo_caja_consolidado'),
    path('cuadre_caja/<int:id>/',CajaViews.CuadreCajaView,name='cuadre_caja'),
    path('borra_pedido_caja/<int:id>/',CajaViews.BorraPedidoCajaView,name='borra_pedido_caja'),
    path('crea_documento_inventarios_pedidos_caja',CajaViews.CreaDocumentosInventariosPedidosCajaView,name='crea_documento_inventarios_pedidos_caja'),
    path('borra_pago_caja/<int:id>/',CajaViews.BorraPagoReciboCajaView,name='borra_pago_caja'),
    path('valida_borrado_pago_caja/<int:id>/',CajaViews.ValidaBorradoPagoReciboCajaView,name='valida_borrado_pago_caja'),
    path('valida_adiciona_item_pedido_caja/<int:id>/',CajaViews.ValidaAdicionaItemPedidoCajaView,name='valida_adiciona_item_pedido_caja'),
    path('adiciona_item_pedido_caja/<int:id>/',CajaViews.AdicionaItemPedidoCajaView,name='adiciona_item_pedido_caja'),
    #path('consolidar_pedidos_caja',CajaViews.ConsolidarPedidosCajaView,name='consolidar_pedidos_caja'), """
    path('pedidos_caja_consolidados/<int:id>/',CajaViews.PedidosCajaConsolidadosView,name='pedidos_caja_consolidados'),
    path('valida_borrado_recibo_caja/<int:id>/',CajaViews.ValidaBorradoReciboCajaView,name='valida_borrado_recibo_caja'),
    path('borra_recibo_caja/<int:id>/',CajaViews.BorraReciboCajaView,name='borra_recibo_caja'),
    #path('seleccion_impresion_pedidos_caja_consolidados',CajaViews.SeleccionImpresionPedidosCajaConsolidadosView,name='seleccion_impresion_pedidos_caja_consolidados'),
    path('busca_pago/',CajaViews.BuscaPagoView,name='busca_pago'),
    path('impresion_pedidos_caja_xls/',CajaViews.ImpresionPedidosCajaXlsView,name='impresion_pedidos_caja_xls'),
    path('impresion_pedidos_caja_consolidado_xls/',CajaViews.ImpresionPedidosCajaConsolidadoXlsView,name='impresion_pedidos_caja_consolidado_xls'),
    path('impresion_pedidos_caja_todos_xls/',CajaViews.ImpresionPedidosCajaTodosXlsView,name='impresion_pedidos_caja_todos_xls'),
    path('impresion_pedido_caja_detalle_xls/<int:id>/',CajaViews.ImpresionPedidoCajaDetalleXlsView,name='impresion_pedido_caja_detalle_xls'),
    path('impresion_pedidos_caja_pdf/',CajaViews.ImpresionPedidosCajaPdfView,name='impresion_pedidos_caja_pdf'),
    path('impresion_pedidos_caja_todos_pdf/',CajaViews.ImpresionPedidosCajaTodosPdfView,name='impresion_pedidos_caja_todos_pdf'),

    path('impresion_pedido_caja_detalle/<int:id>/',CajaViews.ImpresionPedidoCajaDetalleView,name='impresion_pedido_caja_detalle'),
    path('impresion_pedidos_caja_consolidado/',CajaViews.ImpresionPedidosCajaConsolidadoView,name='impresion_pedidos_caja_consolidado'),
    path('impresion_recibo_caja_uno/<int:id>',CajaViews.ImpresionReciboCajaUnoView,name='impresion_recibo_caja_uno'),
    path('impresion_recibos_caja_pdf/',CajaViews.ImpresionRecibosCajaPdfView,name='impresion_recibos_caja_pdf'),
    path('impresion_recibos_caja_todos_pdf/',CajaViews.ImpresionRecibosCajaTodosPdfView,name='impresion_recibos_caja_todos_pdf'),

    path('impresion_recibos_caja_xls',CajaViews.ImpresionRecibosCajaXlsView,name='impresion_recibos_caja_xls'),
    path('impresion_pagos_caja_xls',CajaViews.ImpresionPagosCajaXlsView,name='impresion_pagos_caja_xls'),
    path('impresion_pagos_caja',CajaViews.ImpresionPagosCajaView,name='impresion_pagos_caja'),
    path('impresion_pagos_caja_todos_pdf',CajaViews.ImpresionPagosCajaTodosPdfView,name='impresion_pagos_caja_todos_pdf'),
    path('impresion_cuadre_caja/<int:idcaja>/',CajaViews.ImpresionCuadreCajaView,name='impresion_cuadre_caja'),
    path('impresion_cuadre_caja_xls/<int:idcaja>/',CajaViews.ImpresionCuadreCajaXlsView,name='impresion_cuadre_caja_xls'),
    path('sw_filtro_recibo_caja',CajaViews.SwFiltroReciboCaja,name='sw_filtro_recibo_caja'),
    path ('busca_recibo_caja/<int:id>/',CajaViews.BuscaReciboCajaView,name='busca_recibo_caja'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Sitio Administrativo Hospitality - Plus'