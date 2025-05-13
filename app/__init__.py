from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
        app = Flask(__name__)
        app.config.from_object(config_class)

        from app.models import Workout, Usernames, Friendship, FriendRequest
        db.init_app(app)
        migrate.init_app(app,db)

        from app.routes import routes_blueprint
        app.register_blueprint(routes_blueprint)

        return app