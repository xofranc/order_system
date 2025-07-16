from django.contrib import admin
from .models import Venta, DetalleVenta

# Register your models here.
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0
    readonly_fields = ( 'cantidad', )    
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha', 'usuario')
    list_filter = ('fecha',)
    search_fields = ('producto__nombre', 'usuario__username')
    inlines = [DetalleVentaInline]
    
    def vender_producto(self, request, queryset):
        for venta in queryset:
            try:
                venta.producto.vender(venta.cantidad)
                self.message_user(request, f"Venta de {venta.cantidad} unidades de {venta.producto.nombre} registrada correctamente.")
            except ValueError as e:
                self.message_user(request, str(e), level='error')