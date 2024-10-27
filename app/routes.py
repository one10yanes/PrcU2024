from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory, Response
from app import app, db
from app.models import Usuario
from flask_jwt_extended import create_access_token
from datetime import timedelta
import os
from werkzeug.utils import secure_filename
from .fun_upload_video.vehiculos import Vehiculos
import cv2

vehiculos = Vehiculos()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = Usuario.query.filter_by(nombre_usuario=username).first()

        if user and user.check_password(password):
            access_token = create_access_token(
                identity={'username': user.nombre_usuario, 'is_admin': user.is_admin},
                expires_delta=timedelta(hours=1)
            )
            return jsonify({
                "access_token": access_token,
                "user": {
                    "username": user.nombre_usuario,
                    "is_admin": user.is_admin
                }
            }), 200
        else:
            return jsonify({"msg": "Credenciales inválidas"}), 401

    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('dashboard.html')

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        if 'video' not in request.files:
            return jsonify({"msg": "No se subió ningún video."}), 400
        video_file = request.files['video']
        if video_file.filename == '':
            return jsonify({"msg": "No se seleccionó ningún archivo."}), 400
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        filename = secure_filename(video_file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(video_path)
        return jsonify({"video_url": url_for('video_feed', filename=filename)}), 200
    return render_template('upload_video.html')

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/video_feed/<filename>')
def video_feed(filename):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    cap = cv2.VideoCapture(video_path)

    def generate_frames():
        while True:
            success, frame = cap.read()
            if not success:
                break

            # Procesar el frame usando la lógica de Vehiculos
            frame = vehiculos.procesar_frame(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')