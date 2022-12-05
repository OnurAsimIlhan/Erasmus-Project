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
    from .models import User, Role, University, Course, Todo, Application, ApplicationPeriod, Faq
    with app.app_context():
        db.create_all()
    # ---------------------------------------------------------------------------------------------
    
    # --------------------- Call the Services and connect them with the Models --------------------
    from .services import AuthService, UserService, TodoService, ApplicationService, FaqService, ApplicationPeriodService
    auth_service = AuthService(User, Role)
    user_service = UserService(User)
    todo_service = TodoService(User, Todo)
    application_service = ApplicationService(User, Application)
    application_period_service = ApplicationPeriodService(User, ApplicationPeriod)
    faq_service = FaqService(User, Faq)
    
    
    # ---------------------------------------------------------------------------------------------
    
    # --------------------- Call the Views and connect them with the Services ---------------------
    from .controllers import Login, ErasmusCoordinatorHome, ErasmusCoordinatorViewApplications, CourseCoordinatorController, TodoController, StudentApplicationDetails, FaqFormController
    app.add_url_rule("/login/", view_func=Login.as_view("login", auth_service=auth_service))
    app.add_url_rule("/ec/home", view_func=ErasmusCoordinatorHome.as_view("erasmus_coordinator_homepage", auth_service=auth_service, user_service=user_service, application_period_service=application_period_service))
    app.add_url_rule("/ec/applications/", view_func=ErasmusCoordinatorViewApplications.as_view("erasmus_coordinator_applications", auth_service=auth_service, application_service=application_service))
    app.add_url_rule("/cchome/", view_func=CourseCoordinatorController.as_view("course_coordinator_homepage", auth_service=auth_service))
    app.add_url_rule("/todo/", view_func=TodoController.as_view("todo_page", auth_service=auth_service, todo_service = todo_service))
    app.add_url_rule("/student/application_details", view_func=StudentApplicationDetails.as_view("application_details", auth_service=auth_service))
    app.add_url_rule("/faq/update/department=<department>", view_func=FaqFormController.as_view("faq_form", auth_service=auth_service, user_service=user_service, faq_service=faq_service))
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
