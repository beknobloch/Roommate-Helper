from flask import Flask
from .models import db
from flask_login import LoginManager
import redis
from .config import Config
from flask_migrate import Migrate

login_manager = LoginManager()
cache = None  # Initialized after app is created
migrate = Migrate()

def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    global cache
    cache = redis.Redis(host='redis', port=6379)

    # Register blueprints
    from .routes.homepage import homepage_bp
    from .routes.ledger import ledger_bp
    from .routes.account import account_bp

    app.register_blueprint(homepage_bp)
    app.register_blueprint(ledger_bp)
    app.register_blueprint(account_bp)

    return app

@login_manager.user_loader
def loader_user(user_id):
    from .models import Users
    return Users.query.get(int(user_id))