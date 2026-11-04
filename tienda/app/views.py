from flask import current_app, render_template
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .extensions import appbuilder, db
from .models import Venta, DetalleVenta

class VentaView(ModelView):
    datamodel = SQLAInterface(Venta)
    list_columns = ['fecha', 'cliente', 'monto_total']
    add_columns = ['fecha', 'cliente', 'monto_total']
    edit_columns = ['fecha', 'cliente', 'monto_total']

class DetalleVentaView(ModelView):
    datamodel = SQLAInterface(DetalleVenta)
    list_columns = ['venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    add_columns = ['venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    edit_columns = ['venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal']

appbuilder.add_view(VentaView, "Ventas", category="Gestión Tienda")
appbuilder.add_view(DetalleVentaView, "Detalle de Ventas", category="Gestión Tienda")

@current_app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )