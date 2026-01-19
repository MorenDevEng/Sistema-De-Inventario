from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  
   
   

urlpatterns = [
    path('', views.lista_productos, name='productos'),
    path('producto/<int:producto_id>/editar/', views.editar_producto, name='editar_producto'),
    path('producto/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('crear/', views.crear_producto, name="crear_producto"),
    path('busquedaproducto/', views.busqueda_producto, name='busqueda_producto'),
]
    