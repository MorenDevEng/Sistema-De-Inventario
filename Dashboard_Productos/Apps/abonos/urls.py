from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  
   
   
urlpatterns = [
    path('', views.listado_pagos, name='pagos'),
    path('crear/',views.crear_pago, name="crear_pago"),
    path('busquedapago/', views.busqueda_de_pago, name='buscador_de_pago')
]
    