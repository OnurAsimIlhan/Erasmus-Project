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
    from .models import User, Role
    with app.app_context():
        db.create_all()
    # ---------------------------------------------------------------------------------------------
    
    # --------------------- Call the Services and connect them with the Models --------------------
    from .services import AuthService, AdministratorService, ViewApplicationsService, FinalFormsService
    auth_service = AuthService(User, Role) 
    administrator_service = AdministratorService(User)
    view_applications_service = ViewApplicationsService(User)
    final_forms_service = FinalFormsService(User)
    
    # ---------------------------------------------------------------------------------------------
    
    # --------------------- Call the Views and connect them with the Services ---------------------
    from .controllers import Login, AdministratorController, ViewApplicationsController, FinalFormsController
    app.add_url_rule("/login/", view_func=Login.as_view("login", auth_service=auth_service))
    app.add_url_rule("/administrator_homepage", view_func=AdministratorController.as_view("administrator_homepage", auth_service=auth_service, administrator_service=administrator_service))
    app.add_url_rule("/administrator_view_applications", view_func=ViewApplicationsController.as_view("administrator_view_applications", auth_service = auth_service, view_applications_service = view_applications_service))
    app.add_url_rule("/final_forms", view_func=FinalFormsController.as_view("final_forms", auth_service = auth_service, final_forms_service = final_forms_service))

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
