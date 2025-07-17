from django.contrib import admin
from .models import Venta  # 👈 asegúrate de importar correctamente el modelo


class VentaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'fecha', 'usuario')
    exclude = ('fecha', 'usuario')
    

    class Media:
        js = ('js/admin_insumos.js',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def ver_insumos(self, obj):
        detalles = obj.detalles.all()
        if not detalles:
            return "—"
        return "\n".join(
            [f"{d.cantidad} {d.insumo.unidad} de {d.insumo.nombre}" for d in detalles]
        )
   


admin.site.register(Venta, VentaAdmin)