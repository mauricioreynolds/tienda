from flask import current_app, render_template
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .extensions import appbuilder, db
from .models import Producto, Cliente

class ProductoView(ModelView):
    datamodel = SQLAInterface(Producto)
    list_columns = ['nombre', 'precio_compra', 'precio_venta', 'stock_actual', 'categoria', 'proveedor']
    add_columns = ['nombre', 'precio_compra', 'precio_venta', 'stock_actual', 'categoria', 'proveedor']
    edit_columns = ['nombre', 'precio_compra', 'precio_venta', 'stock_actual', 'categoria', 'proveedor']

class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)
    list_columns = ['nombre', 'telefono', 'nit_ci']
    add_columns = ['nombre', 'telefono', 'nit_ci']
    edit_columns = ['nombre', 'telefono', 'nit_ci']

appbuilder.add_view(ProductoView, "Productos", category="Gestión Tienda")
appbuilder.add_view(ClienteView, "Clientes", category="Gestión Tienda")
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