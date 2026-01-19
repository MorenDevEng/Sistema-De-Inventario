from django.db import models

# Create your models here.

class Cliente(models.Model):
    """Tabla de clientes"""

    nombre = models.CharField(max_length=15)
    apellido = models.CharField(max_length=15, null=True, blank=True)
    telefono = models.BigIntegerField(unique=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.telefono}'
    
    
