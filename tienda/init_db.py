
from app import create_app

from app.extensions import db, appbuilder


app = create_app()


with app.app_context():


    db.create_all()


    role_admin = appbuilder.sm.find_role("Admin")

    if not role_admin:
        print(
            "No se encontro el rol Admin. "
            "Verifica la inicializacion de seguridad."
        )

    else:

        user = appbuilder.sm.find_user(
            username="admin"
        )

        if not user:

            appbuilder.sm.add_user(
                username="admin",
                first_name="Admin",
                last_name="Tienda",
                email="admin@tienda.com",
                role=role_admin,
                password="admin"
            )

            print(
                "Usuario administrador creado correctamente."
            )

        else:

            print(
                "El administrador ya existe. "
                "Base de datos verificada."
            )
