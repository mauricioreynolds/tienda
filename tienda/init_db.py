from app import create_app
from app.extensions import db, appbuilder

app = create_app()

with app.app_context():
    db.create_all()
    
    role_admin = appbuilder.sm.find_role("Admin")
    user = appbuilder.sm.add_user(
        username="admin",
        first_name="Admin",
        last_name="Tienda",
        email="admin@tienda.com",
        role=role_admin,
        password="admin"
    )
    if user:
        print("¡Usuario admin creado con exito!")
    else:
        print("El usuario admin ya existe.")