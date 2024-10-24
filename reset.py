from app import app, db

def crear_base_datos():
    with app.app_context():
        # Elimina la base de datos si existe
        db.drop_all()  
        print("Base de datos eliminada.")

        # Crea una nueva base de datos
        db.create_all()  
        print("Base de datos creada.")

if __name__ == "__main__":
    crear_base_datos()