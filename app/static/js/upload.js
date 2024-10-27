// static/js/upload.js

document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const messageDiv = document.getElementById('message');

    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Evita el comportamiento por defecto del formulario

            const formData = new FormData(uploadForm); // Crea un objeto FormData con el formulario

            try {
                const response = await fetch('/upload_video', {
                    method: 'POST',
                    body: formData // Envía el FormData directamente
                });

                const data = await response.json();

                if (response.ok) {
                    messageDiv.innerHTML = `<div class="alert alert-success">${data.msg}</div>`;
                    // Puedes agregar lógica para limpiar el formulario si es necesario
                    uploadForm.reset();
                } else {
                    messageDiv.innerHTML = `<div class="alert alert-danger">${data.msg}</div>`;
                }
            } catch (error) {
                console.error('Error:', error);
                messageDiv.innerHTML = '<div class="alert alert-danger">Ocurrió un error. Inténtalo de nuevo.</div>';
            }
        });
    }
});
