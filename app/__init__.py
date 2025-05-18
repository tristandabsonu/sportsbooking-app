from flask import Flask
from .models import db
from flask_login import LoginManager
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
    db.init_app(app)

    login_manager = LoginManager(app)
    from .models import User
    @login_manager.user_loader
    def load_user(uid): return User.query.get(int(uid))

    # blueprint registration
    from .auth import auth_bp;     app.register_blueprint(auth_bp)
    from .member import member_bp; app.register_blueprint(member_bp)
    from .admin import admin_bp;   app.register_blueprint(admin_bp)

    return app
