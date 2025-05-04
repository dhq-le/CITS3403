from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()

def create_app():
        app = Flask(__name__)
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SECRET_KEY'] = 'yoursecret-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../database.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        migrate = Migrate(app, db)

        db.init_app(app)

        from app.routes import routes_blueprint
        app.register_blueprint(routes_blueprint)

        return app
