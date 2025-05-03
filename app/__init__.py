from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
        app = Flask(__name__)
        app.config.from_object(Config)
        db.init_app(app)

        from app.routes import routes_blueprint
        app.register_blueprint(routes_blueprint)

        return app
