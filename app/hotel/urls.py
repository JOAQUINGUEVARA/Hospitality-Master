from django.contrib import admin
from django.conf.urls import *
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from profiles.urls import profiles_patterns
from registration.urls import registration_patterns
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from hotel import views as HotelViews


urlpatterns = [
    
    path('tipos_habitacion_list/',HotelViews.TiposHabitacionListView,name='tipos_habitacion_list'),
    path('crea_tipos_habitacion/',HotelViews.CreaTiposHabitacionView.as_view(),name='crea_tipos_habitacion'),
    path('edita_tipos_habitacion/<int:pk>/',HotelViews.EditaTipoHabitacionView.as_view(),name='edita_tipos_habitacion'),
    path('borra_tipos_habitacion/<int:pk>/',HotelViews.BorraTipoHabitacionView.as_view(),name='borra_tipos_habitacion'),

    path('habitaciones_list/',HotelViews.HabitacionesListView,name='habitaciones_list'),
    path('crea_habitacion/',HotelViews.CreaHabitacionView.as_view(),name='crea_habitacion'),
    path('edita_habitacion/<int:pk>/',HotelViews.EditaHabitacionView.as_view(),name='edita_habitacion'),
    path('borra_habitacion/<int:pk>/',HotelViews.BorraHabitacionView.as_view(),name='borra_habitacion'),
    path('impresion_habitaciones_pdf/',HotelViews.ImpresionHabitacionesPdfView,name='impresion_habitaciones_pdf'),
    path('impresion_habitaciones_xls/',HotelViews.ImpresionHabitacionesXlsView,name='impresion_habitaciones_xls'),

    path('reservas_list/',HotelViews.ReservasListView,name='reservas_list'),
    path('reservas_detalle_list/<int:id>/',HotelViews.ReservasDetalleListView,name='reservas_detalle_list'),
    path('valida_reserva/',HotelViews.ValidaReservaView,name='valida_reserva'),
    path('valida_fechas_reserva/',HotelViews.ValidaFechasReservaView,name='valida_fechas_reserva'),
    path('crea_reserva/',HotelViews.CreaReservaView.as_view(),name='crea_reserva'),
    path('edita_reserva/<int:pk>/',HotelViews.EditaReservaView.as_view(),name='edita_reserva'),
    path('borra_reserva/<int:pk>/',HotelViews.BorraReservaView.as_view(),name='borra_reserva'),

    path('registros_list/',HotelViews.RegistrosListView,name='registros_list'),
    path('registro_detalle_list/<int:id>',HotelViews.RegistroDetalleListView,name='registro_detalle_list'),
    path('crea_registro/',HotelViews.CreaRegistroView.as_view(),name='crea_registro'),
    path('edita_registro/<int:pk>/',HotelViews.EditaRegistroView.as_view(),name='edita_registro'),
    path('borra_registro/<int:pk>/',HotelViews.BorraRegistroView.as_view(),name='borra_registro'),
    path('busca_tercero_registro/',HotelViews.BuscaTerceroRegistroView.as_view(),name='busca_tercero_registro'),
    path('crea_tercero_registro/',HotelViews.CreaTerceroRegistroHotelView.as_view(),name='crea_tercero_registro'),
    path('selecciona_tercero_registro/',HotelViews.SeleccionaTerceroRegistroHotelView,name='selecciona_tercero_registro'),
    path('check_out/<int:pk>/',HotelViews.CheckOutView.as_view(),name='check_out'),
    path('valida_pago_estadia/<int:id>',HotelViews.ValidaPagoEstadiaView,name='valida_pago_estadia'),
    path('registro_pedidos_caja_consolidado/<int:id>/',HotelViews.RegistroPedidosCajaConsolidadosView,name='registro_pedidos_caja_consolidado'),
    #path('pago_estadia',HotelViews.PagoEstadiaView,name='pago_estadia'),
    path('pedidos_pendientes_habitacion_list/<int:id>/',HotelViews.PedidosPendientesHabitacionListView,name='pedidos_pendientes_habitacion_list'),
    path('detalle_pedidos_pendientes_habitacion_list/<int:id>/',HotelViews.DetallePedidosPendientesHabitacionListView,name='detalle_pedidos_pendientes_habitacion_list'),
    path('selecciona_caja_recibo_caja_estadia/',HotelViews.SeleccionaCajaReciboCajaEstadiaView,name='selecciona_caja_recibo_caja_estadia'),
    path('liquida_estadia/<int:pk>/',HotelViews.LiquidaEstadiaView.as_view(),name='liquida_estadia'),
    path('valida_creacion_recibo_caja_estadia',HotelViews.ValidaCreacionReciboCajaEstadiaView,name='valida_creacion_recibo_caja_estadia'),
    path('crea_recibo_caja_estadia/<int:id>/',HotelViews.CreaReciboCajaEstadiaView,name='crea_recibo_caja_estadia'),
    path('recibo_caja_hotel/',HotelViews.ReciboCajaHotelView,name='recibo_caja_hotel'),
    #path('recibo_caja_detalle_hotel/<int:id>/',HotelViews.ReciboCajaDetalleHotelView,name='recibo_caja_detalle_hotel'),
    path('valida_borrado_recibo_caja_hotel/<int:id>/',HotelViews.ValidaBorradoReciboCajaHotelView,name='valida_borrado_recibo_caja_hotel'),
    path('borra_recibo_caja_hotel/<int:id>/',HotelViews.BorraReciboCajaHotelView,name='borra_recibo_caja_hotel'),
    path('valida_pago_estadia/<int:id>/',HotelViews.ValidaPagoEstadiaView,name='valida_pago_estadia'),
    path('pago_estadia/',HotelViews.PagoEstadiaView.as_view(),name='pago_estadia'),
    path('ajax_validar_habitacion',HotelViews.AjaxValidarHabitacion,name='ajax_validar_habitacion'),
    path('busca_pago_hotel',HotelViews.BuscaPagoHotelView,name='busca_pago_hotel'),
    path('borra_pago_recibo_caja_hotel/<int:id>/',HotelViews.BorraPagoReciboCajaHotelView,name='borra_pago_recibo_caja_hotel'),
    path('valida_borrado_pago_recibo_caja_hotel/<int:id>/',HotelViews.ValidaBorradoPagoReciboCajaHotelView,name='valida_borrado_pago_recibo_caja_hotel'),
    #path('impresion_recibo_caja_hotel/<int:id>/',HotelViews.ImpresionReciboCajaHotelView,name='impresion_recibo_caja_hotel'),
    path('impresion_pago_recibo_caja_hotel/<int:id>/',HotelViews.ImpresionPagoReciboCajaHotelView,name='impresion_pago_recibo_caja_hotel'),
    path('ajax_habitaciones',HotelViews.AjaxHabitaciones,name='ajax_habitaciones'),
    path('impresion_formato_registro/<int:id>/',HotelViews.ImpresionFormatoRegistroHotelView,name='impresion_formato_registro'),
    path('impresion_pedidos_caja_registro/',HotelViews.ImpresionPedidosCajaRegistroView,name='impresion_pedidos_caja_registro'),
    path('impresion_pedidos_caja_registro_xls/',HotelViews.ImpresionPedidosCajaRegistroXlsView,name='impresion_pedidos_caja_registro_xls'),
    path('acompañante_hotel_list/<int:id>/',HotelViews.AcompañanteHotelListaView,name='acompañante_hotel_list'),
    path('crea_acompañante_hotel/<int:pk>/',HotelViews.CreaAcompañanteHotelView.as_view(),name='crea_acompañante_hotel'),
    path('crea_acompañante_hotel_detalle/',HotelViews.CreaAcompañanteHotelDetalleView,name='crea_acompañante_hotel_detalle'),
    path('edita_acompañante_hotel/<int:pk>/',HotelViews.EditaAcompañanteHotelView.as_view(),name='edita_acompañante_hotel'),
    path('borra_acompañante_hotel/<int:pk>/',HotelViews.BorraAcompañanteView.as_view(),name='borra_acompañante_hotel'),
    path('tercero_edit/<int:id>/',HotelViews.TerceroEditView,name='tercero_edit'),
    path('revisa_tercero/<int:pk>/',HotelViews.RevisaTerceroView.as_view(),name='revisa_tercero'),
    #path('pone_producto_receta',HotelViews.PoneProductoReceta,name='pone_producto_receta'),
    path('impresion_reservas_xls',HotelViews.ImpresionReservasXlsView,name='impresion_reservas_xls'),
    path('impresion_reservas_pdf',HotelViews.ImpresionReservasPdfView,name='impresion_reservas_pdf'),
    path('impresion_registro_xls',HotelViews.ImpresionRegistroXlsView,name='impresion_registro_xls'),
    path('impresion_registro_pdf',HotelViews.ImpresionRegistroPdfView,name='impresion_registro_pdf'),

    path('guarda_fecha_inicial_reserva',HotelViews.GuardaFechaInicialReserva,name='guarda_fecha_inicial_reserva'),
    path('guarda_fecha_final_reserva',HotelViews.GuardaFechaFinalReserva,name='guarda_fecha_final_reserva'),
    path('guarda_habitacion_reserva',HotelViews.GuardaHabitacionReserva,name='guarda_habitacion_reserva'),
    path('guarda_id_registro',HotelViews.GuardaIdRegistro,name='guarda_id_registro'),

    #path('check_in/',HotelViews.CheckInView,name='check_in'),
    #path('check_out/',HotelViews.CheckOutView,name='check_out'),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Sitio Administrativo Hospitality - Plus'  