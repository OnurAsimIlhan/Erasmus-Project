from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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
    from .models import User, Role, University, faq_table, Applications

    with app.app_context():
        db.create_all()
    # ---------------------------------------------------------------------------------------------

    # --------------------- Call the Services and connect them with the Models --------------------
    from .services import (
        AuthService,
        UserService,
        UniversityService,
        FaqService,
        ApplicationsService,
    )

    auth_service = AuthService(User, Role)
    user_service = UserService(User)
    university_service = UniversityService(University)
    faq_service = FaqService(faq_table)
    applications_service = ApplicationsService(application_table=Applications)

    # ---------------------------------------------------------------------------------------------

    # --------------------- Call the Views and connect them with the Services ---------------------
    from .controllers import (
        Login,
        Main,
        Contacts,
        FAQ,
        StudentHome,
        StudentApplication,
        LearningAggrementController,
        PreApprovalController,
    )

    app.add_url_rule("/login/", view_func=Login.as_view("login", auth_service=auth_service))
    app.add_url_rule(
        "/main/", view_func=Main.as_view("main", university_service=university_service)
    )
    app.add_url_rule("/faq/", view_func=FAQ.as_view("faq", faq_service=faq_service))
    app.add_url_rule(
        "/contacts/", view_func=Contacts.as_view("contacts", user_service=user_service)
    )

    app.add_url_rule(
        "/student_home/", view_func=StudentHome.as_view("student_home", auth_service=auth_service)
    )
    app.add_url_rule(
        "/student_application/",
        view_func=StudentApplication.as_view(
            "student_application",
            auth_service=auth_service,
            university_service=university_service,
            applications_service=applications_service,
        ),
    )
    app.add_url_rule(
        "/student_learning_agreement/",
        view_func=LearningAggrementController.as_view(
            "student_learning_agreement",
            auth_service=auth_service,
            applications_service=applications_service,
        ),
    )
    app.add_url_rule(
        "/student_preapproval/",
        view_func=PreApprovalController.as_view(
            "student_preapproval",
            auth_service=auth_service,
            applications_service=applications_service,
            course_service="",
        ),
    )

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
