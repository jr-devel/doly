import os
from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
import app.database as db
import app.log_control as log
from app.models import UserAccount

login_manager = LoginManager()

def register_blueprints(app: Flask) -> None:
    """Registers all blueprints for the Flask application."""
    from app.views import bp as bp_views
    from app.auth import bp as bp_auth
    from app.views_client import bp as bp_views_client
    app.register_blueprint(bp_views)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_views_client)

@login_manager.user_loader
def user_loader(id_user) -> UserAccount:
    return UserAccount.query.get(int(id_user))

def create_app() -> Flask:
    """Creates and configures the Flask DOLY application."""
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    # ----------------- Login Manager ----------------- #
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    # --------------------- Test ---------------------- #
    print(f"SECRET_KEY = {(os.getenv('SECRET_KEY')[:-4]).center(15, '*')}")
    print(f"DATABASE_URL = {(os.getenv('DATABASE_URL')[:10]).center(15,'*')}")
    # ------------------- Blueprints ------------------ #
    register_blueprints(app)
    # -------------- Initialize Database -------------- #
    db.init_db(app)
    # ------------------------------------------------- #
    return app

# Provide a default app instance for Flask CLI / WSGI deployments
app = create_app()