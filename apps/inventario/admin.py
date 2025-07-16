from django.contrib import admin
from .models import Insumo, ActualizacionInventario

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'unidad', 'stock', 'minimo')
    search_fields = ('nombre',)

@admin.register(ActualizacionInventario)
class ActualizacionInventarioAdmin(admin.ModelAdmin):
    list_display = ('insumo', 'tipo', 'cantidad', 'fecha', 'usuario')
    list_filter = ('tipo', 'fecha')
    search_fields = ('insumo__nombre',)
    
