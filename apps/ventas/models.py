from django.db import models
from apps.inventario.models import Insumo, ActualizacionInventario
from apps.accounts.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class Venta(models.Model):
    producto = models.ForeignKey('productos.Productos', on_delete=models.CASCADE, related_name='ventas')
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Venta de {self.cantidad} unidades de {self.producto.nombre} el {self.fecha.strftime("%Y-%m-%d %H:%M:%S")}'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            try:
                self.registrar_venta()
            except ValueError as e:
                raise ValidationError(str(e))
            

    def registrar_venta(self):
        for insumo_relacionado in self.producto.insumos.all():
            cantidad_total = insumo_relacionado.cantidad * self.cantidad

            if insumo_relacionado.insumo.stock < cantidad_total:
                raise ValueError(
                    f'No hay suficiente stock de {insumo_relacionado.insumo.nombre}. '
                    f'Se requieren {cantidad_total} {insumo_relacionado.insumo.unidad}, '
                    f'pero solo hay {insumo_relacionado.insumo.stock}.'
                )

            # Crear movimiento de inventario
            ActualizacionInventario.objects.create(
                insumo=insumo_relacionado.insumo,
                tipo=ActualizacionInventario.SALIDA,
                cantidad=cantidad_total,
                usuario=self.usuario,
                venta=self
            )

            # Registrar detalle de venta
            DetalleVenta.objects.create(
                venta=self,
                insumo=insumo_relacionado.insumo,
                cantidad=cantidad_total
            )

        return f'Se registró correctamente la venta de {self.cantidad} unidades de {self.producto.nombre}.'
    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='detalles_venta')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} {self.insumo.unidad} de {self.insumo.nombre} para la venta {self.venta.id}'
    
    class Meta:
        unique_together = ('venta', 'insumo')  