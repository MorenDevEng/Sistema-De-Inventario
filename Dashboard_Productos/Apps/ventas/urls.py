from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  


urlpatterns = [
    path('', views.lista_ventas, name='ventas'),
    path('crear/', views.crear_venta, name='crear_venta'),
    path('venta/<int:venta_id>/editar/', views.editar_venta),
    path('busquedaventa/', views.busqueda_venta, name='busqueda_venta'),

]
    