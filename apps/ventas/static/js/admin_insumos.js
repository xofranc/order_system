document.addEventListener("DOMContentLoaded", function () {
  const productoSelect = document.getElementById("id_producto");
  if (!productoSelect) return;

  const infoDiv = document.createElement("div");
  infoDiv.id = "info-insumos-live";
  infoDiv.style.marginTop = "10px";
  infoDiv.style.padding = "10px";
  infoDiv.style.border = "1px dashed #888";
  infoDiv.innerHTML = "<em>Selecciona un producto para ver los insumos...</em>";

  // Insertar después del campo producto
  const productoField =
    productoSelect.closest(".form-row") || productoSelect.parentElement;
  productoField.appendChild(infoDiv);

  productoSelect.addEventListener("change", function () {
    const productoId = this.value;
    infoDiv.innerHTML = "Cargando insumos...";

    if (productoId) {
      fetch(`/api/admin/insumos-producto/${productoId}/`)
        .then((res) => res.json())
        .then((data) => {
          if (data.insumos?.length) {
            infoDiv.innerHTML =
              "<strong>Insumos requeridos:</strong><ul>" +
              data.insumos
                .map((i) => `<li>${i.nombre} ( ${i.unidad})</li>`)
                .join("") +
              "</ul>";
          } else {
            infoDiv.innerHTML = "Este producto no tiene insumos asociados.";
          }
        })
        .catch(() => {
          infoDiv.innerHTML = "Error al cargar los insumos.";
        });
    } else {
      infoDiv.innerHTML = "";
    }
  });

  // Disparar el evento una vez al cargar (por si viene ya preseleccionado)
  productoSelect.dispatchEvent(new Event("change"));
});
