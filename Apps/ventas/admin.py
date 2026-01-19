from django.contrib import admin
from .models import Venta, DetalleVenta

# Register your models here.

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_venta', 'total_pagar')
    search_fields = ('cliente__nombre',)
    list_filter = ('fecha_venta',)


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('producto__nombre_producto',)