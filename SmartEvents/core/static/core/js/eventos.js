document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded, looking for counters..."); 
    const contadores = document.querySelectorAll('.contador-evento');

    contadores.forEach(contadorDiv => {
        const fechaEventoString = contadorDiv.dataset.fechaEvento;
        console.log("Found counter div. Date string:", fechaEventoString); 
        if (!fechaEventoString) {
            contadorDiv.textContent = "Fecha no definida";
            console.error("Date string is missing!"); 
            return;
        }

        const fechaEvento = new Date(fechaEventoString).getTime();
        console.log("Parsed date timestamp:", fechaEvento); 

        if (isNaN(fechaEvento)) {
            contadorDiv.textContent = "Error al leer fecha";
            console.error("Failed to parse date string:", fechaEventoString); 
            return; 
        }

        const intervalo = setInterval(() => {
           
            const ahora = new Date().getTime();
            const diferencia = fechaEvento - ahora;

            if (diferencia <= 0) {
                clearInterval(intervalo);
                contadorDiv.textContent = "¡El evento ya comenzó!";
                return;
            }
           
            const dias = Math.floor(diferencia / (1000 * 60 * 60 * 24));
            const horas = Math.floor((diferencia % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutos = Math.floor((diferencia % (1000 * 60 * 60)) / (1000 * 60));
            const segundos = Math.floor((diferencia % (1000 * 60)) / 1000);

            contadorDiv.textContent = `${dias}D: ${horas}H: ${minutos}M: ${segundos}S`;

        }, 1000);
    });
});