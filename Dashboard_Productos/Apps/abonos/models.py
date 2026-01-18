from django.db import models
from Apps.ventas.models import Venta, DetalleVenta
from Apps.clientes.models import Cliente
from django.utils.timezone import now


# Create your models here.

class Pagos(models.Model):
    """Tabla de pagos registrados"""

    numero_factura = models.CharField(max_length=20, unique=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    monto_dolar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField(default=now)
    body = models.TextField(blank=True)
    referencia = models.IntegerField()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.numero_factura:
            self.numero_factura = f"ABON-{self.id:04d}"
            super().save(update_fields=['numero_factura'])

    def __str__(self):
        return f'Factura {self.numero_factura} - Cliente {self.cliente}'

class PagoVenta(models.Model):
    pago = models.ForeignKey(Pagos, on_delete=models.CASCADE, related_name="pago_unico")
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="pagos_ventas")
    monto_aplicado = models.DecimalField(max_digits=10, decimal_places=2)
