from flask import request, jsonify, render_template, redirect, url_for
from app import db
from app.models import Usuario
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app import app  # Importa 'app' después de definirlo en '__init__.py'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', None)
        password = data.get('password', None)
        user = Usuario.query.filter_by(nombre_usuario=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity={'username': user.nombre_usuario, 'is_admin': user.is_admin}, expires_delta=timedelta(hours=1))
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Credenciales inválidas"}), 401
    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('dashboard.html')