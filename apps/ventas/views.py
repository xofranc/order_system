from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Venta  # Importante para acceso al modelo
from apps.productos.models import Productos  # Importa desde app productos si no estaba

@staff_member_required
def admin_obtener_insumos(request, producto_id):
    try:
        producto = Productos.objects.get(pk=producto_id)
        insumos = producto.insumos.all()
        data = [{"nombre": i.insumo.nombre, "unidad": i.insumo.unidad} for i in insumos]
        return JsonResponse({"insumos": data})
    except Productos.DoesNotExist:
        return JsonResponse({"insumos": []})