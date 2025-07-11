"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

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


from core import views as CoreViews
from caja import views as CajaViews
from compras import views as ComprasViews
from cxc import views as CxCViews
from cxp import views as CxPViews
from cocina import views as CocinaViews

#from inventarios import views as InventariosViews
from tesoreria import views as TesoreriaViews
from ventas import views as VentasViews
from hotel import views as HotelViews
from cocina import views as CocinaViews
from registration import views as RegistrationViews
#from inventarios import urls as url_inventarios

app_name = 'core'
#from core.formsets import FormsetDonantePruebaSerologica

urlpatterns = [
    
    path('',CoreViews.HomePageView.as_view(),name=''),
    path('home',CoreViews.HomePageView.as_view(),name='home'),
    path('admin/', admin.site.urls,name='admin'),
    path('registration/', include(registration_patterns)),
    path('profile/', include(profiles_patterns)),
    #path('register', RegistrationViews.register, name='register'),
    path('login/', CoreViews.login, name='login'),
    path('logout', CoreViews.logout, name='logout'),
    path('accounts/reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('menu_caja',CoreViews.MenuCaja.as_view(), name='menu_caja'),
    path('menu_recibos_caja',CoreViews.MenuRecibosCaja.as_view(), name='menu_recibos_caja'),
    path('menu_compras',CoreViews.MenuCompras.as_view(), name='menu_compras'),
    path('menu_cxc',CoreViews.MenuCxC.as_view(), name='menu_cxc'),
    path('menu_cxp',CoreViews.MenuCxP.as_view(), name='menu_cxp'),
    path('menu_inventarios',CoreViews.MenuInventarios.as_view(), name='menu_inventarios'),
    path('menu_tesoreria',CoreViews.MenuTesoreria.as_view(), name='menu_tesoreria'),
    path('menu_ventas',CoreViews.MenuVentas.as_view(), name='menu_ventas'),
    path('menu_procesos',CoreViews.MenuProcesos.as_view(), name='menu_procesos'),
    path('menu_hotel',CoreViews.MenuHotel.as_view(), name='menu_hotel'),
    path('menu_cocina',CoreViews.MenuCocina.as_view(), name='menu_cocina'),

    path("caja/", include("caja.urls")),
    path("inventarios/", include("inventarios.urls")),
    path("core/", include("core.urls")),
    path("compras/", include("compras.urls")),
    path("hotel/", include("hotel.urls")),
    path("cocina/", include("cocina.urls")),
    path("dashboard/", include("dashboard.urls")),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Sitio Administrativo Hospitality - Plus'