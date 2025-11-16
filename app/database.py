import os
from flask import *
from dotenv import load_dotenv
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import app.log_control as log

db = SQLAlchemy()

def init_db(app:Flask):
    """Initializes the database with the Flask application."""
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

def test_conn() -> bool:
    """Tests the database connection using SQLAlchemy."""
    try:
        engine = create_engine(os.getenv('DATABASE_URL'))
        with engine.connect() as conn:
            version = conn.execute(text("SELECT version()")).scalar()
            log.log_info(f"Database version: {version}")
            log.log_info(f"Database connection successful.")
        return True
    except Exception as e:
        log.log_error(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    log.log_info(f"SQLALCHEMY_DATABASE_URI = {os.getenv('DATABASE_URL')}")
    log.log_info("Database connection test: " + ("Passed" if test_conn() else "Failed"))
    init_db(Flask(__name__))