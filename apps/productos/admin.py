from django.contrib import admin, messages
from .models import Productos, ProductoInsumo
from apps.inventario.models import ActualizacionInventario
from django.utils.timezone import now


class ProductoInsumoInline(admin.TabularInline):
    model = ProductoInsumo
    extra = 3
    min_num = 1
    autocomplete_fields = ['insumo']


@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'activo')
    inlines = [ProductoInsumoInline]
    actions = ['vender_producto']

    def vender_producto(self, request, queryset):
        for producto in queryset:
            resultado = producto.vender()
            if "Error" in resultado:
                messages.warning(request, f"{producto.nombre}: {resultado}")
            else:
                messages.success(request, f"{producto.nombre}: {resultado}")

    vender_producto.short_description = "Vender 1 unidad del producto seleccionado"