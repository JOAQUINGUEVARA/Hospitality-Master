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

from core import views as CoreViews 

urlpatterns = [
    
    path('terceros_list/',CoreViews.TerceroListView,name='terceros_list'),
    path('detalle_tercero/<int:id>/',CoreViews.DetalleTerceroView,name='detalle_tercero'),
    path('crea_tercero/',CoreViews.CreaTerceroView.as_view(),name='crea_tercero'),
    path('edita_tercero/<int:pk>/',CoreViews.EditaTerceroView.as_view(),name='edita_tercero'),
    path('borra_tercero/<int:pk>/',CoreViews.BorraTerceroView.as_view(),name='borra_tercero'),
    #path('impresion_terceros_pdf/',CoreViews.ImpresionTercerosPdfView,name='impresion_terceros_pdf'),
    path('impresion_terceros_xls/',CoreViews.ImpresionTercerosXlsView,name='impresion_terceros_xls'),   
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Sitio Administrativo Hospitality - Plus'    


