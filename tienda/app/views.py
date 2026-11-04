from flask import current_app, render_template
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .extensions import appbuilder, db
from .models import Categoria, Proveedor

class CategoriaView(ModelView):
    datamodel = SQLAInterface(Categoria)
    list_columns = ['nombre']
    add_columns = ['nombre']
    edit_columns = ['nombre']

class ProveedorView(ModelView):
    datamodel = SQLAInterface(Proveedor)
    list_columns = ['nombre', 'telefono', 'direccion']
    add_columns = ['nombre', 'telefono', 'direccion']
    edit_columns = ['nombre', 'telefono', 'direccion']

appbuilder.add_view(CategoriaView, "Categorías", category="Gestión Tienda")
appbuilder.add_view(ProveedorView, "Proveedores", category="Gestión Tienda")

@current_app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )