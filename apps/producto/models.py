from django.db import models
from apps.inventario.models import Insumos
# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    actvo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
class RecetaProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='recetas')
    insumo = models.ForeignKey(Insumos, on_delete=models.CASCADE, related_name='recetas')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'{self.producto.nombre} usa {self.insumo.nombre} un valor de ({self.cantidad})' 
    
 