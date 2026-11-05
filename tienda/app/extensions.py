
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()

appbuilder = AppBuilder()

csrf = CSRFProtect()
