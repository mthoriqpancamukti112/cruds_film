# [IMPORT LIBRARY]
from flask import Flask                      # Framework utama web
from flask_sqlalchemy import SQLAlchemy      # ORM untuk database
from flask_login import LoginManager         # Modul login user
from config import Config                    # File konfigurasi

# [INIT OBJEK GLOBAL]
db = SQLAlchemy()                            # Objek database global
login_manager = LoginManager()               # Objek login global

# [FACTORY FUNCTION]
def create_app(config_class=Config):
    app = Flask(__name__)                    # Inisialisasi Flask app
    
    # [LOAD KONFIGURASI]
    app.config.from_object(config_class)     # Ambil konfigurasi dari config.py

    # [INIT EXTENSIONS]
    db.init_app(app)                         # Inisialisasi SQLAlchemy
    login_manager.init_app(app)              # Inisialisasi Flask-Login

    # [LOGIN MANAGER CONFIG]
    login_manager.login_view = 'auth.login'                      # Redirect ke 'auth.login' saat belum login
    login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'  # Pesan default
    login_manager.login_message_category = 'warning'             # Kategori flash message

    # [LOAD USER SESSION]
    from .models import Admin               # Import model Admin (harus punya `get_id`)
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))  # Ambil user dari ID (untuk session login)

    # [REGISTER ROUTES / BLUEPRINTS]
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)   # Blueprint utama (user/public)

    from app.admin_routes import admin_bp
    app.register_blueprint(admin_bp)         # Blueprint admin

    from app.auth_routes import auth_bp
    app.register_blueprint(auth_bp)          # Blueprint otentikasi (login/logout/register)

    return app                                # Return objek app
