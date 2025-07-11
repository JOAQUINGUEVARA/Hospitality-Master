from django.urls import include, path
from compras import views as ComprasViews
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from profiles.urls import profiles_patterns
from registration.urls import registration_patterns
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views 

urlpatterns = [
path('proveedores_list/',ComprasViews.ProveedoresListView,name='proveedores_list'),
path('detalle_proveedor/<int:id>',ComprasViews.DetalleProveedorView,name='detalle_proveedor'),
path('crea_proveedor/',ComprasViews.CreaProveedorView.as_view(),name='crea_proveedor'),
path('edita_proveedor/<int:pk>/',ComprasViews.EditaProveedorView.as_view(),name='edita_proveedor'),
path('borra_proveedor/<int:pk>/',ComprasViews.BorraProveedorView.as_view(),name='borra_proveedor'),

path('ordenes_compra_list/',ComprasViews.OrdenesCompraListView,name='ordenes_compra_list'),
path('detalle_orden_compra/<int:id>',ComprasViews.DetalleOrdenCompraView,name='detalle_orden_compra'),
path('crea_orden_compra/',ComprasViews.CreaOrdenCompraView.as_view(),name='crea_orden_compra'),
path('edita_orden_compra/<int:pk>/',ComprasViews.EditaOrdenCompraView.as_view(),name='edita_orden_compra'),
path('valida_editar_orden_compra_detalle/<int:id>/',ComprasViews.ValidaEditarOrdenCompraDetalleView,name='valida_editar_orden_compra_detalle'),
path('edita_orden_compra_detalle/<int:pk>/',ComprasViews.EditaOrdenCompraDetalleView.as_view(),name='edita_orden_compra_detalle'),
path('confirma_borrado_orden_compra/<int:id>/',ComprasViews.ConfirmaBorradoOrdenCompraView,name='confirma_borrado_orden_compra'),
path('borra_orden_compra/<int:id>/',ComprasViews.BorraOrdenCompraView,name='borra_orden_compra'),
path('confirma_borrado_orden_compra_detalle/<int:id>/',ComprasViews.ConfirmaBorradoOrdenCompraDetalleView,name='confirma_borrado_orden_compra_detalle'),
path('borra_orden_compra_detalle/<int:id>/',ComprasViews.BorraOrdenCompraDetalleView,name='borra_orden_compra_detalle'),
path('verifica_detalle_orden_compra/<int:id>/',ComprasViews.VerificaDetalleOrdenCompraView,name='verifica_detalle_orden_compra'),
path('selecciona_item_orden_compra/<int:id>/',ComprasViews.SeleccionaItemOrdenCompraView,name='selecciona_item_orden_compra'),
path('filtra_item_orden_compra/',ComprasViews.FiltraItemOrdenCompraView.as_view(),name='filtra_item_orden_compra'),
path('guarda_item_orden',ComprasViews.GuardaItemOrdenCompra,name='guarda_item_orden'),
path('guarda_id_orden',ComprasViews.GuardaIdOrden,name='guarda_id_orden'),
path('guarda_id_orden_detalle',ComprasViews.GuardaIdOrdenCompraDetalle,name='guarda_id_orden_detalle'),
path('valida_crea_detalle_orden_compra/<int:id>/',ComprasViews.ValidaCreaDetalleOrdenCompraView,name='valida_crea_detalle_orden_compra'),
path('crea_detalle_orden_compra/<int:id>/',ComprasViews.CreaDetalleOrdenCompraView,name='crea_detalle_orden_compra'),
path('datos_empaque',ComprasViews.DatosEmpaqueView,name='datos_empaque'),
path('selecciona_proveedor_orden_compra/',ComprasViews.SeleccionaProveedorOrdenCompra,name='selecciona_proveedor_orden_compra'),
path('busca_proveedor_orden_compra/',ComprasViews.BuscaProveedorOrdenCompra.as_view(),name='busca_proveedor_orden_compra'),
path('crea_proveedor_orden_compra/',ComprasViews.CreaProveedorOrdenCompraView.as_view(),name='crea_proveedor_orden_compra'),
path('direcciona_orden_compra/<int:id>/',ComprasViews.DireccionaOrdenCompraView,name='direcciona_orden_compra'),
path('obtener_unidad_medida',ComprasViews.ObtenerUnidadMedidaView,name='obtener_unidad_medida'),
path('despachos_list/',ComprasViews.DespachosListView,name='despachos_list'),
path('busca_orden_compra/',ComprasViews.BuscaOrdenCompraDespacho.as_view(),name='busca_orden_compra'),
path('selecciona_orden_compra/',ComprasViews.SeleccionaOrdenCompra,name='selecciona_orden_compra'),

path('detalle_despacho/<int:id>',ComprasViews.DetalleDespachoView,name='detalle_despacho'),
path('crea_despacho/',ComprasViews.CreaDespachoView.as_view(),name='crea_despacho'),
path('valida_crea_despacho/',ComprasViews.ValidaCreaDespachoView,name='valida_crea_despacho'),
path('edita_despacho/<int:pk>/',ComprasViews.EditaDespachoView.as_view(),name='edita_despacho'),
path('verifica_detalle_despacho/<int:id>',ComprasViews.VerificaDetalleDespachoView,name='verifica_detalle_despacho'),
path('crea_detalle_despacho/<int:id>/',ComprasViews.CreaDetalleDespachoView,name='crea_detalle_despacho'),
#path('edita_despacho_detalle/<int:pk>/',ComprasViews.EditaDespachoDetalleView.as_view(),name='edita_despacho_detalle'),
path('confirma_borrado_despacho/<int:id>/',ComprasViews.ConfirmaBorradoDespachoView,name='confirma_borrado_despacho'),
path('borra_despacho/<int:id>/',ComprasViews.BorraDespachoView,name='borra_despacho'),
#path('borra_despacho_detalle/<int:id>/',ComprasViews.BorraDespachoDetalleView,name='borra_despacho_detalle'),
path('guarda_id_despacho',ComprasViews.GuardaIdDespacho,name='guarda_id_despacho'),
path('guarda_id_despacho_detalle',ComprasViews.GuardaIdDespachoDetalle,name='guarda_id_despacho_detalle'),
path('direcciona_despacho/<int:id>',ComprasViews.DireccionaDespachoView,name='direcciona_despacho'),
path('datos_despacho_detalle',ComprasViews.DatosDespachoDetalleView,name='datos_despacho_detalle'),
path('guarda_cantidad_enviada',ComprasViews.GuardaCantidadEnviadaView,name='guarda_cantidad_enviada'),
path('impresion_ordenes_compra',ComprasViews.ImpresionOrdenesCompraView,name='impresion_ordenes_compra'),
path('impresion_ordenes_compra_xls',ComprasViews.ImpresionOrdenesCompraXlsView,name='impresion_ordenes_compra_xls'),
path('impresion_detalle_orden_compra_xls',ComprasViews.ImpresionDetalleOrdenCompraXlsView,name='impresion_detalle_orden_compra_xls'),
path('impresion_detalle_orden_compra_pdf',ComprasViews.ImpresionDetalleOrdenCompraPdfView,name='impresion_detalle_orden_compra_pdf'),
path('impresion_despacho',ComprasViews.ImpresionDespachoView,name='impresion_despacho'),
path('impresion_despacho_xls',ComprasViews.ImpresionDespachoXlsView,name='impresion_despacho_xls'),
path('proveedor_item',ComprasViews.ProveedorItemView,name='proveedor_item'),
path('impresion_proveedores_xls',ComprasViews.ImpresionProveedoresXlsView,name='impresion_proveedores_xls'),
path('impresion_item_proveedor_xls',ComprasViews.ImpresionItemProveedorXlsView,name='impresion_item_proveedor_xls'),
path('impresion_item_proveedor',ComprasViews.ImpresionItemProveedorView,name='impresion_item_proveedor'),


#path('confirma_borrado_despacho_detalle/<int:id>/',ComprasViews.ConfirmaBorradoDespachoDetalleView,name='confirma_borrado_despacho_detalle'),
#path('borra_despacho_detalle/<int:id>/',ComprasViews.BorraDespachoDetalleView,name='borra_despacho_detalle'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Sitio Administrativo Hospitality - Plus'    