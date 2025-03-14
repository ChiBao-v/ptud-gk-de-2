from flask import Flask
import os
from dotenv import load_dotenv
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

load_dotenv()
SECRET_KEY = os.environ.get("KEY")
DB_NAME = os.environ.get("DB_NAME")

def create_database(app):
    if not os.path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created DB!")

def create_admin():
    """Tạo tài khoản admin mặc định nếu chưa tồn tại."""
    from .models import User  # Import User để tránh lỗi vòng lặp
    with db.session.begin():  # Dùng begin() để đảm bảo giao dịch
        if not User.query.filter_by(email="admin@example.com").first():
            admin_user = User(
                email="admin@example.com",
                user_name="admin",
                password=generate_password_hash("admin123"),  # Đặt mật khẩu mặc định
                is_admin=True
            )
            db.session.add(admin_user)
            print("✅ Created default admin user!")

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  

    db.init_app(app)

    from .models import Note, User  

    create_database(app)

    # Đăng ký các blueprint
    from .user import user
    from .views import views
    from .admin import admin_bp  

    app.register_blueprint(user)
    app.register_blueprint(views)
    app.register_blueprint(admin_bp, url_prefix='/admin')  

    login_manager = LoginManager()
    login_manager.login_view = "user.login"
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes=1)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Tạo tài khoản admin khi khởi động ứng dụng
    with app.app_context():
        create_admin()

    @app.context_processor
    def inject_user():
        return dict(user=current_user)

    return app





