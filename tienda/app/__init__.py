from flask import Flask, redirect
from .extensions import db, appbuilder, csrf


def create_app():
    app = Flask(__name__)

    app.config.from_object("config")

    app.config["AUTH_TYPE"] = 1

    app.config["FAB_INDEX_VIEW"] = "app.home.MiTiendaIndexView"

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from . import models

        appbuilder.init_app(app, db.session)

        db.create_all()

        from . import views

    return app