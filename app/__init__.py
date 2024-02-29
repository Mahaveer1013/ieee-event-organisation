#__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_mail import Mail
from sqlalchemy import create_engine

# Initialize SQLAlchemy
db = SQLAlchemy()
DB_NAME = "database.db"
mail = None

def create_app():
    global mail
    
    app = Flask(__name__, static_folder='static')
    
    # Configure the app
    app.config['SECRET_KEY'] = '#$&^&^WYYDUHS&YWE'
    db_path = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_path, DB_NAME)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    UPLOAD_FOLDER = os.path.join(app.root_path, 'static/img')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'kklimited1013@gmail.com'  
    app.config['MAIL_PASSWORD'] = 'hmupzeoeftrbzmkl' 
    # Initialize Flask-Mail
    mail = Mail(app)
    


    # Import and initialize Flask-SocketIO with the app
    from . import models
    from .models import Admin
    models.db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))
    
    create_database(app)
    # Import and register blueprints
    from .auth import auth
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    return app

# Function to create the database if it doesn't exist
def create_database(app):
    if not os.path.exists(os.path.join(app.instance_path, DB_NAME)):
        with app.app_context():
            db.create_all()
        print('Created Database!')


