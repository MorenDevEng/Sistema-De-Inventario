from django.db import models
from django.utils import timezone
from Apps.clientes.models import Cliente

# Create your models here.

class Producto(models.Model):
    """Tabla de los productos"""
    nombre_producto = models.CharField(max_length=100, unique=True)
    precio_dolar = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    imagen = models.URLField(blank=True, null=True, help_text="URL de la imagen del producto")
    cantidad = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'{self.nombre_producto} - Precio: {self.precio_dolar} USD - Cantidad: {self.cantidad}'
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre_producto']
