from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.listar_clientes, name='clientes'),
    path('crear/', views.crear_cliente, name='crear_cliente'),
    path('editarCliente/<int:id>/', views.editar_cliente, name='editarcliente'),
    path('eliminarCliente/<int:id>/', views.eliminar_cliente),
    path('buscarclientes/', views.busqueda_cliente, name='busqueda_cliente'),


]