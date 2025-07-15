from django.db import models
from django.utils import timezone
from apps.accounts.models import User

# Create your models here.
class Insumos(models.Model):
    nombre = models.CharField(max_length=100)
    unidad = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)
    minimo = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return f'{self.nombre} ({self.unidad}) - Stock: {self.stock}'   
    
    def actualizar_stock(self, cantidad, tipo):
        if tipo == 'entrada':
            self.stock += cantidad
        elif tipo == 'salida':
            if self.stock < cantidad:
                raise ValueError(f'Stock insuficiente para realizar la salida de {cantidad} {self.unidad} de {self.nombre}. Stock actual: {self.stock}')
            self.stock -= cantidad
        self.save()
    
class MovimientoInsumo(models.Model):
    ENTRADA = 'entrada'
    SALIDA = 'salida'
    TIPO_CHOICES = [
        (ENTRADA, 'Entrada'),
        (SALIDA, 'Salida'),
    ]
    
    insumo = models.ForeignKey(Insumos, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.tipo == self.ENTRADA:
            self.insumo.stock += self.cantidad
        elif self.tipo == self.SALIDA:
            if self.insumo.stock < self.cantidad:
                raise ValueError(f'No hay suficiente stock de {self.insumo.nombre} para realizar la salida. Stock actual: {self.insumo.stock}, requerido: {self.cantidad}')
            self.insumo.stock -= self.cantidad
        self.insumo.save()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.tipo.capitalize()} de {self.cantidad} {self.insumo.unidad} de {self.insumo.nombre} el {self.fecha.strftime("%Y-%m-%d %H:%M:%S")}'