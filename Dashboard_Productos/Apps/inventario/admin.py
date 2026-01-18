from django.contrib import admin
from .models import Producto

# Register your models here.

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre_producto', 'precio_dolar', 'cantidad')
    list_filter = ('nombre_producto',)
    list_editable = ('precio_dolar', 'cantidad')

