
from datetime import date, datetime, time, timedelta

from flask import (
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app
)

from flask_appbuilder import (
    ModelView,
    BaseView,
    expose
)

from flask_appbuilder.models.sqla.interface import SQLAInterface

from sqlalchemy import func

from .extensions import appbuilder, db

from .ai_assistant import consultar_groq

from .models import (
    Categoria,
    Proveedor,
    Producto,
    Cliente,
    Venta,
    DetalleVenta
)




class CategoriaModelView(ModelView):

    datamodel = SQLAInterface(Categoria)

    list_columns = ['nombre']

    add_columns = ['nombre']

    edit_columns = ['nombre']




class ProveedorModelView(ModelView):

    datamodel = SQLAInterface(Proveedor)

    list_columns = [
        'nombre',
        'telefono',
        'direccion'
    ]

    add_columns = [
        'nombre',
        'telefono',
        'direccion'
    ]

    edit_columns = add_columns




class ProductoModelView(ModelView):

    datamodel = SQLAInterface(Producto)

    list_columns = [
        'nombre',
        'precio_compra',
        'precio_venta',
        'stock_actual',
        'categoria',
        'proveedor'
    ]

    add_columns = [
        'nombre',
        'precio_compra',
        'precio_venta',
        'stock_actual',
        'categoria',
        'proveedor'
    ]

    edit_columns = add_columns




class ClienteModelView(ModelView):

    datamodel = SQLAInterface(Cliente)

    list_columns = [
        'nombre',
        'telefono',
        'nit_ci'
    ]

    add_columns = [
        'nombre',
        'telefono',
        'nit_ci'
    ]

    edit_columns = add_columns




class VentaCarritoView(BaseView):

    route_base = "/carrito-compras"

    @expose("/", methods=["GET", "POST"])
    def carrito(self):

        carrito = session.get("carrito_compras", {})

        if request.method == "POST":

            accion = request.form.get("accion")

            if accion == "agregar":

                try:

                    producto_id = int(
                        request.form.get("producto_id")
                    )

                    cantidad = int(
                        request.form.get("cantidad")
                    )

                    if cantidad <= 0:
                        raise ValueError(
                            "La cantidad debe ser mayor a cero."
                        )

                    producto = db.session.get(
                        Producto,
                        producto_id
                    )

                    if not producto:

                        flash(
                            "El producto no existe.",
                            "danger"
                        )

                    else:

                        clave = str(producto_id)

                        cantidad_actual = int(
                            carrito.get(clave, 0)
                        )

                        nueva_cantidad = (
                            cantidad_actual + cantidad
                        )

                        if nueva_cantidad > producto.stock_actual:

                            flash(
                                f"Stock insuficiente para "
                                f"{producto.nombre}. "
                                f"Disponible: {producto.stock_actual}",
                                "danger"
                            )

                        else:

                            carrito[clave] = nueva_cantidad

                            session["carrito_compras"] = carrito

                            session.modified = True

                            flash(
                                "Producto agregado correctamente.",
                                "success"
                            )

                except (ValueError, TypeError):

                    flash(
                        "Selecciona un producto y una cantidad válida.",
                        "danger"
                    )

            elif accion == "actualizar":

                try:

                    producto_id = int(
                        request.form.get("producto_id")
                    )

                    cantidad = int(
                        request.form.get("cantidad")
                    )

                    producto = db.session.get(
                        Producto,
                        producto_id
                    )

                    if not producto or cantidad <= 0:

                        raise ValueError(
                            "Producto o cantidad no válidos."
                        )

                    if cantidad > producto.stock_actual:

                        flash(
                            f"Stock insuficiente. "
                            f"Disponible: {producto.stock_actual}",
                            "danger"
                        )

                    else:

                        carrito[str(producto_id)] = cantidad

                        session["carrito_compras"] = carrito

                        session.modified = True

                        flash(
                            "Cantidad actualizada correctamente.",
                            "success"
                        )

                except (ValueError, TypeError):

                    flash(
                        "No se pudo actualizar la cantidad.",
                        "danger"
                    )

            elif accion == "eliminar":

                producto_id = request.form.get("producto_id")

                carrito.pop(str(producto_id), None)

                session["carrito_compras"] = carrito

                session.modified = True

                flash(
                    "Producto eliminado del carrito.",
                    "info"
                )

            elif accion == "vaciar":

                session.pop("carrito_compras", None)

                carrito = {}

                flash(
                    "Carrito vaciado correctamente.",
                    "info"
                )

            elif accion == "finalizar":

                try:

                    cliente_id = int(
                        request.form.get("cliente_id")
                    )

                    cliente = db.session.get(
                        Cliente,
                        cliente_id
                    )

                    if not cliente:
                        raise ValueError(
                            "Debes seleccionar un cliente válido."
                        )

                    if not carrito:
                        raise ValueError(
                            "No hay productos en el carrito."
                        )

                    detalles_preparados = []

                    total_venta = 0.0

                    for producto_id in sorted(
                        carrito.keys(),
                        key=int
                    ):

                        cantidad = int(
                            carrito[producto_id]
                        )

                        if cantidad <= 0:
                            raise ValueError(
                                "Existe una cantidad no válida."
                            )

                        producto = (
                            db.session.query(Producto)
                            .filter(
                                Producto.id == int(producto_id)
                            )
                            .with_for_update()
                            .first()
                        )

                        if not producto:

                            raise ValueError(
                                "Uno de los productos ya no existe."
                            )

                        if producto.stock_actual < cantidad:

                            raise ValueError(
                                f"Stock insuficiente para "
                                f"{producto.nombre}. "
                                f"Disponible: {producto.stock_actual}"
                            )

                        precio = float(
                            producto.precio_venta
                        )

                        subtotal = precio * cantidad

                        detalles_preparados.append(
                            (
                                producto,
                                cantidad,
                                precio,
                                subtotal
                            )
                        )

                        total_venta += subtotal

                    nueva_venta = Venta(
                        cliente=cliente,
                        monto_total=round(total_venta, 2)
                    )

                    db.session.add(nueva_venta)

                    db.session.flush()

                    for (
                        producto,
                        cantidad,
                        precio,
                        subtotal
                    ) in detalles_preparados:

                        detalle = DetalleVenta(
                            venta=nueva_venta,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=precio,
                            subtotal=round(subtotal, 2)
                        )

                        db.session.add(detalle)

                        producto.stock_actual -= cantidad

                    db.session.commit()

                    venta_id = nueva_venta.id

                    session.pop("carrito_compras", None)

                    flash(
                        f"Venta N.º {venta_id} registrada "
                        f"correctamente. Total: Bs "
                        f"{total_venta:.2f}",
                        "success"
                    )

                    return redirect(
                        url_for("VentaCarritoView.carrito")
                    )

                except (ValueError, TypeError) as error:

                    db.session.rollback()

                    flash(
                        str(error),
                        "danger"
                    )

                except Exception:

                    db.session.rollback()

                    current_app.logger.exception(
                        "Error al finalizar la venta"
                    )

                    flash(
                        "No se pudo finalizar la venta. "
                        "No se confirmaron los cambios.",
                        "danger"
                    )

            else:

                flash(
                    "Acción no reconocida.",
                    "warning"
                )

            return redirect(
                url_for("VentaCarritoView.carrito")
            )

        productos = (
            db.session.query(Producto)
            .order_by(Producto.nombre)
            .all()
        )

        clientes = (
            db.session.query(Cliente)
            .order_by(Cliente.nombre)
            .all()
        )

        items = []

        total = 0.0

        cantidad_total = 0

        for producto_id, cantidad in carrito.items():

            producto = db.session.get(
                Producto,
                int(producto_id)
            )

            if producto:

                cantidad = int(cantidad)

                precio = float(
                    producto.precio_venta
                )

                subtotal = precio * cantidad

                items.append({
                    "producto": producto,
                    "cantidad": cantidad,
                    "precio": precio,
                    "subtotal": subtotal
                })

                total += subtotal

                cantidad_total += cantidad

        return self.render_template(
            "venta_carrito.html",
            productos=productos,
            clientes=clientes,
            items=items,
            total=round(total, 2),
            cantidad_total=cantidad_total
        )




class VentaHistorialView(ModelView):

    datamodel = SQLAInterface(Venta)

    base_permissions = [
        'can_list',
        'can_show'
    ]

    list_columns = [
        'id',
        'fecha',
        'cliente',
        'monto_total'
    ]

    show_columns = [
        'id',
        'fecha',
        'cliente',
        'monto_total',
        'detalles'
    ]




class ReporteDetallesView(ModelView):

    datamodel = SQLAInterface(DetalleVenta)

    base_permissions = [
        'can_list',
        'can_show',
        'can_export'
    ]

    list_title = "Reporte General de Productos Vendidos"

    list_columns = [
        'venta',
        'producto',
        'cantidad',
        'precio_unitario',
        'subtotal'
    ]




class AsistenteIAView(BaseView):

    route_base = "/asistente-ia"

    default_view = "chat"

    @expose("/", methods=["GET", "POST"])
    def chat(self):

        mensajes = session.get("chat_mi_tienda", [])

        if request.method == "POST":

            pregunta = request.form.get(
                "mensaje", ""
            ).strip()

            if not pregunta:
                flash(
                    "Escribe una pregunta.",
                    "warning"
                )

                return redirect(
                    url_for("AsistenteIAView.chat")
                )

            try:

                hoy = date.today()

                inicio_hoy = datetime.combine(
                    hoy,
                    time.min
                )

                fin_hoy = inicio_hoy + timedelta(days=1)

                inicio_mes = datetime(
                    hoy.year,
                    hoy.month,
                    1
                )

                if hoy.month == 12:

                    inicio_mes_siguiente = datetime(
                        hoy.year + 1,
                        1,
                        1
                    )

                else:

                    inicio_mes_siguiente = datetime(
                        hoy.year,
                        hoy.month + 1,
                        1
                    )

                ventas_hoy = (
                    db.session.query(
                        func.coalesce(
                            func.sum(Venta.monto_total), 0
                        )
                    )
                    .filter(
                        Venta.fecha >= inicio_hoy,
                        Venta.fecha < fin_hoy
                    )
                    .scalar()
                )

                ventas_mes = (
                    db.session.query(
                        func.coalesce(
                            func.sum(Venta.monto_total), 0
                        )
                    )
                    .filter(
                        Venta.fecha >= inicio_mes,
                        Venta.fecha < inicio_mes_siguiente
                    )
                    .scalar()
                )

                cantidad_ventas = (
                    db.session.query(Venta).count()
                )

                productos = (
                    db.session.query(Producto)
                    .order_by(Producto.stock_actual.asc())
                    .limit(30)
                    .all()
                )

                inventario = [
                    {
                        "producto": p.nombre,
                        "stock": p.stock_actual,
                        "precio_compra": float(p.precio_compra),
                        "precio_venta": float(p.precio_venta)
                    }
                    for p in productos
                ]

                mas_vendidos = (
                    db.session.query(
                        Producto.nombre,
                        func.sum(
                            DetalleVenta.cantidad
                        ).label("cantidad")
                    )
                    .join(
                        DetalleVenta,
                        DetalleVenta.producto_id == Producto.id
                    )
                    .group_by(
                        Producto.id,
                        Producto.nombre
                    )
                    .order_by(
                        func.sum(
                            DetalleVenta.cantidad
                        ).desc()
                    )
                    .limit(5)
                    .all()
                )

                resumen = f"""
INFORMACIÓN REAL DE MI TIENDA:

Fecha actual: {hoy}

Ventas de hoy: Bs {float(ventas_hoy):.2f}

Ventas del mes: Bs {float(ventas_mes):.2f}

Cantidad total de ventas registradas: {cantidad_ventas}

INVENTARIO:
{inventario}

PRODUCTOS MÁS VENDIDOS:
{[
    {
        "producto": nombre,
        "unidades_vendidas": int(cantidad)
    }
    for nombre, cantidad in mas_vendidos
]}
"""

                historial = [
                    {
                        "role": "system",
                        "content": (
                            "Eres el asistente inteligente de Mi Tienda, "
                            "un micromercado. Responde en español, "
                            "de forma clara, breve y sencilla. "
                            "Utiliza los datos reales proporcionados "
                            "para responder preguntas sobre ventas, "
                            "inventario y productos. "
                            "No inventes cifras. "
                            "Si no tienes información suficiente, "
                            "dilo claramente. "
                            "Tu función es exclusivamente de consulta. "
                            "No puedes registrar, modificar ni eliminar "
                            "información de la base de datos."
                        )
                    },
                    {
                        "role": "system",
                        "content": resumen
                    }
                ]

                historial.extend(mensajes[-10:])

                historial.append({
                    "role": "user",
                    "content": pregunta
                })

                respuesta = consultar_groq(historial)

                mensajes.append({
                    "role": "user",
                    "content": pregunta
                })

                mensajes.append({
                    "role": "assistant",
                    "content": respuesta
                })

                session["chat_mi_tienda"] = mensajes[-12:]

                session.modified = True

            except Exception:

                current_app.logger.exception(
                    "Error en el asistente IA"
                )

                flash(
                    "No se pudo obtener una respuesta. "
                    "Intenta nuevamente.",
                    "danger"
                )

            return redirect(
                url_for("AsistenteIAView.chat")
            )

        return self.render_template(
            "asistente_ia.html",
            mensajes=mensajes
        )




appbuilder.add_view(
    CategoriaModelView,
    "Categorías",
    icon="fa-tags",
    category="Gestión Tienda"
)

appbuilder.add_view(
    ProveedorModelView,
    "Proveedores",
    icon="fa-truck",
    category="Gestión Tienda"
)

appbuilder.add_view(
    ProductoModelView,
    "Productos",
    icon="fa-box",
    category="Gestión Tienda"
)

appbuilder.add_view(
    ClienteModelView,
    "Clientes",
    icon="fa-users",
    category="Gestión Tienda"
)

appbuilder.add_view(
    VentaCarritoView,
    "Realizar Venta",
    href="/carrito-compras/",
    icon="fa-shopping-cart",
    category="Gestión Tienda"
)

appbuilder.add_view(
    VentaHistorialView,
    "Historial de Ventas",
    icon="fa-history",
    category="Gestión Tienda"
)

appbuilder.add_view(
    ReporteDetallesView,
    "Reporte de Ventas",
    icon="fa-file-text",
    category="Gestión Tienda"
)

appbuilder.add_view(
    AsistenteIAView,
    "Asistente IA",
    icon="fa-comments",
    category="Gestión Tienda"
)
