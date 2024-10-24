// scripts.js

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const messageDiv = document.getElementById('message');

            try {
                const response = await fetch('/login', {  // Cambiado de '/auth/login' a '/login'
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (response.status === 200) {
                    // Almacena el token en el localStorage o en una cookie
                    localStorage.setItem('access_token', data.access_token);
                    messageDiv.innerHTML = '<div class="alert alert-success">Login exitoso. Redirigiendo...</div>';
                    // Redirige al panel de administración
                    window.location.href = '/admin/dashboard';
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