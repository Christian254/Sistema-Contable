from __future__ import unicode_literals
from __future__ import absolute_import #importamos ambas lineas para que no se generen errores

from django.conf.urls import url
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import *

app_name = 'contable'
admin.autodiscover()


urlpatterns = [
    url(r'^login/$', views.auth_login,name="authentication"),
    url(r'^registrarse/$', views.auth_signup,name="authentication"),
    url(r'^logout/$',auth_views.logout, {'next_page':'/'}, name='logout'),
    url(r'^$', index),
    url(r'^kardex/', kardex),
    url(r'^OF/', OF, name='OF'),
    url(r'^(?P<of_id>[0-9]+)/terminar/$',terminar, name="terminar"), 
    url(r'^(?P<of_id>[0-9]+)/ver/$',ver, name="ver"), 
    url(r'^(?P<kardex_id>[0-9]+)/CostoPromedio/$',CP, name="CostoPromedio"), 
    url(r'^ingresarCuenta/', ingresarCuenta),
    url(r'^(?P<grupo_id>[0-9]+)/insertCuenta/$',insertCuenta, name="insertCuenta"),
    url(r'^nuevoPeriodo/', nuevoPeriodo,name="nuevoPeriodo"),
    url(r'^(?P<periodo_id>[0-9]+)/reg_transaccion/$',reg_transaccion, name='reg_transaccion'),#Registro de transacciones 
    url(r'^(?P<periodo_id>[0-9]+)/estados/$',estados, name='estados'),#Mostrar los estados financieros 
    url(r'^puestos/$', conPuestos , name='con_puestos'),#Registro de transacciones
    url(r'^nuevo-puesto/$', ingresarPuesto , name='in_puestos'),#Registro de transacciones
    url(r'^editar-puesto/(?P<id_puesto>\d+)/$', editPuesto , name='edit_puestos'),#Registro de transacciones
    url(r'^planilla/$', conPlanilla, name='con_planilla'),#Registro de transacciones
    url(r'^sistema-salarial/$', menuSisPlanilla, name='menu_planilla'),#Registro de transacciones
    url(r'^planilla-areas/$', areaPlanilla, name='area_planilla'),#Registro de transacciones
    url(r'^admin-planilla/(?P<id_planilla>\d+)/$', adminPlanilla , name='admin_planilla'),#Registro de transacciones
    url(r'^depreciacion/$', depreciacion , name='depreciacion'),
    url(r'^amortizacion/$', amortizacion , name='amortizacion'),
    url(r'^agotamiento/$', agotamiento , name='agotamiento'),
    url(r'^adelantado/$', adelantado , name='adelantado'),
    url(r'^gacumulado/$', gacumulado , name='gacumulado'),
    url(r'^eliminar-planilla/(?P<id_planilla>\d+)/$', elmPlanilla , name='elm_planilla'),#Registro de transacciones
    url(r'^sancionar-planilla/(?P<id_planilla>\d+)/$', sanPlanilla , name='san_planilla'),#Registro de transacciones
    url(r'^prorrateo/$', conProrrateo , name='con_prorrateo'),#Consultar prorrateo
]

