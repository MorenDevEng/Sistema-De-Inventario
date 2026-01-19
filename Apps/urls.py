from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view),
    path('clientes/', include('Apps.clientes.urls')),
    path('productos/', include('Apps.inventario.urls')),
    path('ventas/', include('Apps.ventas.urls')),
    path('pagos/', include('Apps.abonos.urls')),

]
