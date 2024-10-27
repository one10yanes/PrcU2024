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
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();

                if (response.ok) {
                    // Solo almacena el JWT en el localStorage
                    localStorage.setItem('access_token', data.access_token);
                    messageDiv.innerHTML = '<div class="alert alert-success">Login exitoso. Redirigiendo...</div>';
                    // Redirige al dashboard
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
