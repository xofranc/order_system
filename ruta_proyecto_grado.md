# 🎓 Proyecto de Grado - Sistema Integrado de Ventas, Inventario, Membresías y ML

Este documento define la hoja de ruta completa para el desarrollo de un sistema unificado de gestión de ventas, stock, membresías y predicción de demanda, con interfaz animada mediante GSAP.

---

## 🔧 ETAPA 1: Núcleo funcional de ventas e inventario

| Tarea                    | Estado   | Notas                           |
| ------------------------ | -------- | ------------------------------- |
| Registro de ventas       | ✅ Listo | Descuento automático de insumos |
| Actualización de stock   | ✅ Listo | Vía `ActualizacionInventario`   |
| Relación producto-insumo | ✅ Listo | Usando `ProductoInsumo`         |
| Validación de stock      | ✅ Listo | Error si stock insuficiente     |
| Visualización en admin   | ✅ Listo | `ver_insumos`, sin inlines      |

---

## ▶️ ETAPA 2: Reportes y control de mermas

| Tarea                       | Prioridad | Notas                               | especificaciones                                         |
| --------------------------- | --------- | ----------------------------------- | -------------------------------------------------------- |
| Reporte de ventas por fecha | Alta      | Filtro por rango, PDF o tabla       |
| Reporte de stock actual     | Alta      | Productos e insumos disponibles     |
| Registro de mermas          | Alta      | Manual o desde cocina/admin         | solo pueden agregar mermas, el cocinero, o administrador |
| Historial de movimientos    | Media     | Basado en `ActualizacionInventario` |
| Exportar reportes PDF/Excel | Media     | Incluye ventas, stock, mermas       |
| Alertas de stock mínimo     | Media     | Notificaciones o marcación visual   |

---

## ▶️ ETAPA 3: Usuarios y roles

| Tarea                                 | Prioridad | Notas                                           |
| ------------------------------------- | --------- | ----------------------------------------------- |
| Definir roles (admin, mesero, cocina) | Alta      | Puede hacerse con `user_type` o `groups`        |
| Asignar vistas y permisos             | Alta      | Cada usuario accede a su panel                  |
| Dashboard por rol                     | Media     | KPIs según funciones (ventas, pedidos, alertas) |
| Autenticación y control de acceso     | Alta      | Login + redirección por tipo                    |

---

## 📅 ETAPA 4: Pantallas operativas internas

| Tarea                | Prioridad | Notas                                        |
| -------------------- | --------- | -------------------------------------------- |
| Pantalla de cocina   | Alta      | Solo visualiza pedidos en tiempo real        |
| App web para meseros | Alta      | Registro de pedidos y cobro                  |
| Vista de productos   | Alta      | Consulta fácil y rápida por parte del mesero |
| Estado del pedido    | Media     | (pendiente, listo, entregado)                |

---

## ✨ ETAPA 5: Sistema de membresías

| Tarea                          | Prioridad | Notas                                  |
| ------------------------------ | --------- | -------------------------------------- |
| Modelo de membresía/cliente    | Alta      | Datos personales y relación con ventas |
| Registro de puntos/beneficios  | Media     | Por monto o frecuencia de compras      |
| Visual estilo Wallet (QR/pase) | Media     | Para usar desde celular                |
| Aplicación de descuentos       | Media     | En ventas relacionadas a membresía     |

---

## 🧠 ETAPA 6: Machine Learning

| Tarea                            | Prioridad | Notas                                |
| -------------------------------- | --------- | ------------------------------------ |
| Predicción de ventas             | Media     | Por producto, basado en historial    |
| Sugerencia automática de compras | Media     | Según demanda esperada               |
| Clasificación por rotación       | Media     | Identificar productos sin movimiento |
| Rentabilidad por producto        | Media     | Precio vs insumos utilizados         |

---

## 🌐 ETAPA 7: Interfaz web animada (GSAP)

| Tarea                              | Prioridad | Notas                         |
| ---------------------------------- | --------- | ----------------------------- |
| Página principal animada           | Media     | Estilo visual tipo lookbook   |
| Navegación animada entre secciones | Media     | Transiciones suaves           |
| Vista de productos animada         | Baja      | Integración de fetch con GSAP |
| Integración con membresías/login   | Baja      | Entrada a portal              |

---

## 🔗 Extra: API REST (Django REST Framework)

| Tarea                               | Prioridad | Notas                                     |
| ----------------------------------- | --------- | ----------------------------------------- |
| Endpoint de productos               | Baja      | Para frontend JS o apps                   |
| Endpoint de ventas                  | Media     | Si frontend se separa o se crea app móvil |
| Endpoint de membresías              | Media     | Para consultar puntos, QR, etc.           |
| Endpoint de reportes y predicciones | Media     | Si se requiere dashboard externo          |

---

## 📆 Siguiente paso actual:

> Terminar completamente el módulo de **ventas** y luego pasar a:
>
> - Reportes de ventas y stock.
> - Registro y control de mermas.

---

Este roadmap se actualizará conforme avances.
