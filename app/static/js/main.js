document.addEventListener('DOMContentLoaded', function () {
    // Referencias a los enlaces del menú
    const registerCamera = document.getElementById('register-camera');
    const viewCamera = document.getElementById('view-camera');
    const uploadVideo = document.getElementById('upload-video');
    const viewViolations = document.getElementById('view-violations');
    const viewVehicles = document.getElementById('view-vehicles');
    const assignCameras = document.getElementById('assign-cameras');
    const manageUsers = document.getElementById('manage-users');
    
    // Contenedor donde se cargará el contenido dinámico
    const contentContainer = document.getElementById('dashboard-content');

    // Función para cargar el contenido
    function loadContent(content) {
        contentContainer.innerHTML = `<h3>${content}</h3><p>Contenido relacionado con ${content}.</p>`;
    }

    // Event listeners para los clics en el menú
    registerCamera.addEventListener('click', () => loadContent('Registrar Cámara'));
    viewCamera.addEventListener('click', () => loadContent('Ver Cámara'));
    uploadVideo.addEventListener('click', () => loadContent('Subir Video'));
    viewViolations.addEventListener('click', () => loadContent('Ver Infracciones'));
    viewVehicles.addEventListener('click', () => loadContent('Ver Vehículos'));
    assignCameras.addEventListener('click', () => loadContent('Asignar Cámaras'));
    manageUsers.addEventListener('click', () => loadContent('Gestionar Usuarios'));
});
