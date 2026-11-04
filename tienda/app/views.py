from flask import current_app, render_template
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .extensions import appbuilder, db
from .models import Producto, Cliente

# --- VENTANA 3: Productos ---
class ProductoView(ModelView):
    datamodel = SQLAInterface(Producto)
    list_columns = ['nombre', 'precio_compra', 'precio_venta', 'stock_actual', 'categoria', 'proveedor']
    add_columns = ['nombre', 'precio_compra', 'precio_venta', 'stock_actual', 'categoria', 'proveedor']
    edit_columns = ['nombre', 'precio_compra', 'precio_venta', 'stock_actual', 'categoria', 'proveedor']

# --- VENTANA 4: Clientes ---
class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)
    list_columns = ['nombre', 'telefono', 'nit_ci']
    add_columns = ['nombre', 'telefono', 'nit_ci']
    edit_columns = ['nombre', 'telefono', 'nit_ci']

# Registrar solo las ventanas 3 y 4
appbuilder.add_view(ProductoView, "Productos", category="Gestión Tienda")
appbuilder.add_view(ClienteView, "Clientes", category="Gestión Tienda")

@current_app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )