from django.db import models
from apps.inventario.models import Insumo, ActualizacionInventario

# Create your models here.

class Productos(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    def add_producto(self, nombre, precio, descripcion=None):
        producto = Productos(nombre=nombre, precio=precio, descripcion=descripcion)
        producto.save()
        return producto
    
    def descontar_insumos(self, cantidad=1):
        for insumo_relacionado in self.insumos.all():
            insumo_relacionado.descontar_insumo(cantidad_producto=cantidad)

    def vender(self, cantidad=1):
        print(f">>> [DEBUG] Ejecutando vender({cantidad}) para {self.nombre}")
        try:
            self.descontar_insumos(cantidad=cantidad)
            return f'Se vendieron {cantidad} unidades de {self.nombre} y se descontaron los insumos correctamente.'
        except ValueError as e:
            return f'Error al vender producto: {str(e)}'
        
class ProductoInsumo(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='insumos')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, related_name='productos')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.cantidad} {self.insumo.unidad} de {self.insumo.nombre} para {self.producto.nombre}'
    
    def descontar_insumo(self, cantidad_producto=1):
        cantidad_total = self.cantidad * cantidad_producto

        if self.insumo.stock < cantidad_total:
            raise ValueError(
                f'No hay suficiente stock de {self.insumo.nombre}. '
                f'Se requieren {cantidad_total} {self.insumo.unidad}, '
                f'pero solo hay {self.insumo.stock}.'
            )

        # Aquí ya no se descuenta, porque ActualizacionInventario lo hará
        ActualizacionInventario.objects.create(
            insumo=self.insumo,
            tipo=ActualizacionInventario.SALIDA,
            cantidad=cantidad_total,
            usuario=None  # Puedes ajustar esto si tienes acceso al usuario actual
        )