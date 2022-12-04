from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required, logout_user
from flask import Flask


db = SQLAlchemy()

def create_app():
    # --------------------------------------- Create app ------------------------------------------ 
    app = Flask(__name__, template_folder="../website/templates")
    app.config["SECRET_KEY"] = "secretkey"
    # ---------------------------------------------------------------------------------------------
    
    # --------------------------- Database initialization | configuration -------------------------
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///../website/database.db"
    db.init_app(app)
    # ---------------------------------------------------------------------------------------------
    
    # -------------------- Call the Models and create the tables or the database ------------------
    from .models import User, Role, University,faq_table
    with app.app_context():
        db.create_all()
       
        
        
        

    # ---------------------------------------------------------------------------------------------
    
    # --------------------- Call the Services and connect them with the Models --------------------
    from .services import AuthService
    auth_service = AuthService(User, Role)
    from .services import UserService
    user_service = UserService(User)
    from .services import UniversityService
    university_service = UniversityService(University)
    from .services import FaqService
    faq_service = FaqService(faq_table)
    
    # ---------------------------------------------------------------------------------------------
    
    # --------------------- Call the Views and connect them with the Services ---------------------
    

    from .controllers import Login
    app.add_url_rule("/login/", view_func=Login.as_view("login", auth_service=auth_service))

    from .controllers import Main
    app.add_url_rule("/main/", view_func=Main.as_view("main", university_service=university_service))

    from .controllers import FAQ
    app.add_url_rule("/faq/", view_func=FAQ.as_view("faq", faq_service=faq_service))

    from .controllers import Contacts
    app.add_url_rule("/contacts/", view_func=Contacts.as_view("contacts", user_service=user_service))
    
    # ---------------------------------------------------------------------------------------------
    
    # ------------------------------------- Login Manager -----------------------------------------
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(bilkent_id):
        return User.query.get(int(bilkent_id))
    # ---------------------------------------------------------------------------------------------
    
    return app
