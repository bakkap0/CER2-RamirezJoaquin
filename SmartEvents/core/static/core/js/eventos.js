document.addEventListener("DOMContentLoaded", () => {

    const contadores = document.querySelectorAll('.contador-evento');

    contadores.forEach(contadorDiv => {
        
        const fechaEventoString = contadorDiv.dataset.fechaEvento;

        if (!fechaEventoString) {
            contadorDiv.textContent = "Fecha no definida";
            return; 
        }

        const fechaEvento = new Date(fechaEventoString).getTime();

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
