from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import path


db = SQLAlchemy()

def create_app():
    # Create app 
    app = Flask(__name__, template_folder="../website/templates")
    app.config["SECRET_KEY"] = "secretkey"

    # Database initialization/configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///../website/database.db"
    db.init_app(app)

    # Call Models and create the tables or the database
    from .models import User, Role
    with app.app_context():
        db.create_all()
        
    # To be Continued...
    
    # Call Services and conncet them with the Models
    from .services import AuthService
    auth_service = AuthService(User, Role) 
    
    # Call Views and connect them with the Services
    from .controllers import Login
    app.add_url_rule("/login/", view_func=Login.as_view("login", auth_service=auth_service))


    return app