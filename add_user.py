from app import app, db
from app.models import Usuario

def crear_usuario_admin():
    with app.app_context():
        # Verifica si ya existe un usuario administrador
        admin = Usuario.query.filter_by(nombre_usuario='admin').first()
        if admin:
            print("El usuario administrador ya existe.")
        else:
            # Crea un nuevo usuario administrador
            nuevo_admin = Usuario(
                nombre_usuario='adm',
                correo='admin@admin.com',
                is_admin=True
            )
            nuevo_admin.set_password('1234')  # Establece la contraseña del administrador
            db.session.add(nuevo_admin)
            db.session.commit()
            print("Usuario administrador creado exitosamente.")

if __name__ == "__main__":
    crear_usuario_admin()