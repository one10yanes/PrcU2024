from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__, instance_relative_config=True)
import os

# Asegúrate de que esto esté en el archivo donde inicializas tu Flask app
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')  # Cambia 'uploads' si necesitas otro nombre

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database-name.db'  # Añade tu URI de base de datos aquí
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Añade tu clave secreta JWT aquí




db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)  # Inicializa JWTManager con la aplicación Flask

from app import routes, models  # Importa routes y models