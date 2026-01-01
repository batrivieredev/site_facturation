from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import Config

# Initialize extensions
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from flask import request, redirect, url_for
    from flask_login import current_user
    @app.before_request
    def require_login():
        allowed_routes = ['auth.login', 'static']
        if not current_user.is_authenticated and request.endpoint not in allowed_routes:
            return redirect(url_for('auth.login'))

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        from flask import redirect, url_for
        return redirect(url_for('dashboard.dashboard'))

    # Register blueprints here
    from app.routes.dashboard import dashboard_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.client import client_bp
    from app.routes.invoice import invoice_bp
    from app.routes.mailing import mailing_bp
    from app.routes.settings import settings_bp
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(mailing_bp)
    app.register_blueprint(settings_bp)

    return app
