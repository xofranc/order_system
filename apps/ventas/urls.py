from django.urls import path
from .views import admin_obtener_insumos

urlpatterns = [
    path('api/admin/insumos-producto/<int:producto_id>/', admin_obtener_insumos, name='admin_insumos_producto'),
]