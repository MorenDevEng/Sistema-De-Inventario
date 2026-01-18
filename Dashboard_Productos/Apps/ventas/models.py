from django.db import models
from Apps.clientes.models import Cliente
from Apps.inventario.models import Producto  

# Create your models here.

class Venta(models.Model):
    """Tabla de ventas"""

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas_clientes')
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ('PAGADO', 'Pagado'),
        ('PARCIAL_50', 'Parcial 50%'),
        ('PENDIENTE', 'Pendiente'),
    ], default='PENDIENTE')

    def __str__(self):
        return f'Venta #{self.id} de {self.cliente.nombre} - Total: {self.total_pagar} - Estado: {self.estado}'
    
   

class DetalleVenta(models.Model):
    """Tabla de detalles de venta"""

    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.producto.nombre_producto} - {self.cantidad} x {self.precio_unitario} = {self.subtotal}'


