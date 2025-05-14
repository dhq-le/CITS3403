from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os #maybe no need
from app.config import Config
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'routes.login'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    from app.models import Usernames
    return Usernames.query.get(int(user_id))

def create_app(config_class=None):
        from app.config import Config
        if config_class is None:
            config_class = Config
        app = Flask(__name__)
        app.config.from_object(config_class)

        from app.models import Workout, Usernames, Friendship, FriendRequest
        db.init_app(app)
        migrate.init_app(app,db)

        login_manager.init_app(app)

        from app.routes import routes_blueprint
        app.register_blueprint(routes_blueprint)

        return app