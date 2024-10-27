document.addEventListener('DOMContentLoaded', () => {
    const uploadVideo = document.getElementById('upload-video');

    if (uploadVideo) {
        uploadVideo.addEventListener('click', (event) => {
            event.preventDefault(); // Previene la navegación normal
            loadContent('upload_video'); // Carga el contenido de la ruta
        });
    }

    // Función para cargar contenido dinámicamente
    async function loadContent(route) {
        const contentDiv = document.getElementById('content'); // Asegúrate de tener un div con este ID
        contentDiv.innerHTML = ''; // Limpia el contenido previo

        try {
            const response = await fetch(`/${route}`); // Supone que tienes una ruta como /upload_video
            const data = await response.text();

            if (response.ok) {
                contentDiv.innerHTML = data; // Carga el contenido recibido
                initUploadVideo(); // Inicializa la lógica del upload_video si es necesario
            } else {
                contentDiv.innerHTML = '<div class="alert alert-danger">Error al cargar el contenido.</div>';
            }
        } catch (error) {
            console.error('Error:', error);
            contentDiv.innerHTML = '<div class="alert alert-danger">Ocurrió un error al cargar el contenido.</div>';
        }
    }
});

