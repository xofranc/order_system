from django.db import models
from apps.inventario.models import Insumo, ActualizacionInventario
from apps.accounts.models import User

# Create your models here.
class Venta(models.Model):
    producto = models.ForeignKey('productos.Productos', on_delete=models.CASCADE, related_name='ventas')
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Venta de {self.cantidad} unidades de {self.producto.nombre} el {self.fecha.strftime("%Y-%m-%d %H:%M:%S")}'
    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='detalles_venta')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} {self.insumo.unidad} de {self.insumo.nombre} para la venta {self.venta.id}'
    
    class Meta:
        unique_together = ('venta', 'insumo')  # Evita duplicados en la misma venta