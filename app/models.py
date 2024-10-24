from datetime import datetime
from app import db  # Importa la instancia de SQLAlchemy desde tu app Flask
from werkzeug.security import generate_password_hash, check_password_hash  # Importa las funciones necesarias


# Tabla 'usuarios'
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(64), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.nombre_usuario}>'

# Tabla 'camaras'
class Camara(db.Model):
    __tablename__ = 'camaras'
    camara_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camara_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    status = db.Column(db.Enum('active', 'inactive', 'maintenance'), nullable=False)
    last_online = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    eventos = db.relationship("Evento", backref="camara")
    grabaciones = db.relationship("Grabacion", backref="camara")
    transmisiones_en_vivo = db.relationship("TransmisionEnVivo", backref="camara")
    vehiculos_detectados = db.relationship("VehiculoDetectado", backref="camara")
    usuario_camaras = db.relationship("UsuarioCamara", backref="camara")

# Tabla 'eventos'
class Evento(db.Model):
    __tablename__ = 'eventos'
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camaras.camara_id'), nullable=False)
    event_type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    event_time = db.Column(db.DateTime, default=datetime.utcnow)

# Tabla 'grabaciones'
class Grabacion(db.Model):
    __tablename__ = 'grabaciones'
    recording_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camaras.camara_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    format = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabla 'logs'
class Log(db.Model):
    __tablename__ = 'logs'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))  # Cambiado de 'usuarios.user_id' a 'usuarios.id'
    action = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Tabla 'transmisiones_en_vivo'
class TransmisionEnVivo(db.Model):
    __tablename__ = 'transmisiones_en_vivo'
    live_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    camera_id = db.Column(db.Integer, db.ForeignKey('camaras.camara_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    stream_url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum('active', 'ended', 'failed'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Tabla 'usuario_camara'
class UsuarioCamara(db.Model):
    __tablename__ = 'usuario_camara'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)  # Cambiado de 'usuarios.user_id' a 'usuarios.id'
    camara_id = db.Column(db.Integer, db.ForeignKey('camaras.camara_id'), nullable=True)

# Tabla 'vehiculos_detectados'
class VehiculoDetectado(db.Model):
    __tablename__ = 'vehiculos_detectados'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    placa = db.Column(db.String(20), nullable=False)
    velocidad = db.Column(db.DECIMAL(5, 2), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    infraccion = db.Column(db.Boolean, default=False)
    observaciones = db.Column(db.Text)
    camara_id = db.Column(db.Integer, db.ForeignKey('camaras.camara_id'))