const btn = document.getElementById("publicarBtn");
const nombreInput = document.getElementById("nombreInput");
const comentarioInput = document.getElementById("comentario");
const lista = document.getElementById("comentariosUl");

btn.addEventListener("click", () => {
  const nombre = nombreInput.value.trim();
  const comentario = comentarioInput.value.trim();

  if (nombre && comentario) {
    const fecha = new Date();
    const fechaStr = fecha.toLocaleString("es-CL", {
      dateStyle: "short",
      timeStyle: "short"
    });

    const li = document.createElement("li");
    li.classList.add("list-group-item");
    li.innerHTML = `
      <div class="d-flex justify-content-between align-items-baseline mb-1">
        <strong>${nombre}</strong>
        <small class="text-muted">${fechaStr}</small>
      </div>
      <div>${comentario}</div>
    `;

    lista.appendChild(li);
    nombreInput.value = "";
    comentarioInput.value = "";
  } else {
    alert("Por favor, completa ambos campos.");
  }
});
