from django.test import TestCase
from django.urls import reverse
from apps.inventario.models import Insumos, MovimientoInsumo

# Create your tests here.

class InsumosTests(TestCase):
    def setUp(self):
        self.insumo = Insumos.objects.create(nombre='Test Insumo', unidad='kg', stock=100, minimo=10)
    
    def test_insumo_str(self):
        self.assertEqual(str(self.insumo), 'Test Insumo (kg) - Stock: 100')
    
    def test_actualizar_stock(self):
        self.insumo.actualizar_stock(20, 'salida')
        self.assertEqual(self.insumo.stock, 80)
    
    def test_movimiento_insumo_entrada(self):
        movimiento = MovimientoInsumo.objects.create(insumo=self.insumo, tipo=MovimientoInsumo.ENTRADA, cantidad=20)
        self.assertEqual(movimiento.insumo.stock, 120)
    
    def test_movimiento_insumo_salida(self):
        movimiento = MovimientoInsumo.objects.create(insumo=self.insumo, tipo=MovimientoInsumo.SALIDA, cantidad=30)
        self.assertEqual(movimiento.insumo.stock, 70)
    
    def test_movimiento_insumo_salida_insuficiente_stock(self):
        with self.assertRaises(ValueError):
            MovimientoInsumo.objects.create(insumo=self.insumo, tipo=MovimientoInsumo.SALIDA, cantidad=200)
