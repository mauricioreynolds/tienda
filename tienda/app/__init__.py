
from flask import Flask

from .extensions import db, appbuilder, csrf


def create_app():

    app = Flask(__name__)

    app.config.from_object("config")

    db.init_app(app)

    csrf.init_app(app)

    with app.app_context():

        from . import models

        appbuilder.init_app(app, db.session)

        db.create_all()

        from . import views

    return app
