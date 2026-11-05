from app import create_app
from app.extensions import db, appbuilder
from app.models import Categoria, Proveedor, Producto, Cliente, Venta, DetalleVenta

app = create_app()

with app.app_context():
    db.create_all()
    
    role_admin = appbuilder.sm.find_role("Admin")

    user = appbuilder.sm.find_user(username="admin")
    if not user:
        appbuilder.sm.add_user(
            username="admin",
            first_name="Admin",
            last_name="Tienda",
            email="admin@tienda.com",
            role=role_admin,
            password="admin"
        )
        print("Usuario admin creado exitosamente.")
    else:
        print("Tablas creadas en MySQL exitosamente.")