from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from config import Config
from extensions import db, bcrypt, csrf
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_login import LoginManager
import os

csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Khởi tạo extensions
    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    Migrate(app, db)

    # Import routes sau khi khởi tạo
    from routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from models import NhanSu
    @login_manager.user_loader
    def load_user(id):
        return NhanSu.query.get(id)

    return app

app = create_app()
