from flask import Flask
from .extensions import db, appbuilder

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")

    db.init_app(app)

    with app.app_context():
        # Importar explícitamente las clases para registrar el metadata en SQLAlchemy
        from app.models import Categoria, Proveedor, Producto, Cliente, Venta, DetalleVenta  # noqa: F401

        db.create_all()

        appbuilder.init_app(app, db.session)
        from . import views  # noqa: F401

    return app