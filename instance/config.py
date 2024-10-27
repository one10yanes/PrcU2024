import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mydatabase.db'  # Asegúrate de que esta línea sea correcta
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'tu_clave_jwt'
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
