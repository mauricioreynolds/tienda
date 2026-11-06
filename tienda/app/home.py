
from datetime import date, datetime, time, timedelta

from flask import g, redirect, request
from flask_appbuilder import IndexView, expose
from sqlalchemy import func

from .extensions import db
from .models import Producto, Cliente, Venta


class MiTiendaIndexView(IndexView):

    index_template = "dashboard.html"

    @expose("/")
    def index(self):


        if not getattr(g.user, "is_authenticated", False):
            return redirect(
                self.appbuilder.get_url_for_login_with(request.url)
            )


        hoy = date.today()

        inicio_hoy = datetime.combine(hoy, time.min)
        fin_hoy = inicio_hoy + timedelta(days=1)

        inicio_mes = datetime(hoy.year, hoy.month, 1)

        if hoy.month == 12:
            inicio_mes_siguiente = datetime(hoy.year + 1, 1, 1)
        else:
            inicio_mes_siguiente = datetime(
                hoy.year, hoy.month + 1, 1
            )

        ventas_hoy = (
            db.session.query(
                func.coalesce(func.sum(Venta.monto_total), 0)
            )
            .filter(
                Venta.fecha >= inicio_hoy,
                Venta.fecha < fin_hoy
            )
            .scalar()
        )

        ventas_mes = (
            db.session.query(
                func.coalesce(func.sum(Venta.monto_total), 0)
            )
            .filter(
                Venta.fecha >= inicio_mes,
                Venta.fecha < inicio_mes_siguiente
            )
            .scalar()
        )

        total_productos = db.session.query(Producto).count()
        total_clientes = db.session.query(Cliente).count()
        total_ventas = db.session.query(Venta).count()

        productos_bajos = (
            db.session.query(Producto)
            .filter(Producto.stock_actual <= 5)
            .order_by(Producto.stock_actual.asc())
            .limit(5)
            .all()
        )

        cantidad_stock_bajo = (
            db.session.query(Producto)
            .filter(Producto.stock_actual <= 5)
            .count()
        )

        ultimas_ventas = (
            db.session.query(Venta)
            .order_by(Venta.fecha.desc())
            .limit(5)
            .all()
        )

        etiquetas_grafico = []
        valores_grafico = []

        for dias_atras in range(6, -1, -1):

            dia = hoy - timedelta(days=dias_atras)

            inicio_dia = datetime.combine(dia, time.min)
            fin_dia = inicio_dia + timedelta(days=1)

            total_dia = (
                db.session.query(
                    func.coalesce(
                        func.sum(Venta.monto_total), 0
                    )
                )
                .filter(
                    Venta.fecha >= inicio_dia,
                    Venta.fecha < fin_dia
                )
                .scalar()
            )

            etiquetas_grafico.append(
                dia.strftime("%d/%m")
            )

            valores_grafico.append(
                float(total_dia or 0)
            )

        return self.render_template(
            self.index_template,
            appbuilder=self.appbuilder,
            ventas_hoy=float(ventas_hoy or 0),
            ventas_mes=float(ventas_mes or 0),
            total_productos=total_productos,
            total_clientes=total_clientes,
            total_ventas=total_ventas,
            productos_bajos=productos_bajos,
            cantidad_stock_bajo=cantidad_stock_bajo,
            ultimas_ventas=ultimas_ventas,
            etiquetas_grafico=etiquetas_grafico,
            valores_grafico=valores_grafico,
            fecha_actual=hoy
        )
