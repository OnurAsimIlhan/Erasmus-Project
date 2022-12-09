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
    from .models import User, Role, University, Course, Todo, Applications, ApplicationPeriod, Faq

    with app.app_context():
        db.create_all()
    # ---------------------------------------------------------------------------------------------

    # --------------------- Call the Services and connect them with the Models --------------------
    from .services import (
        AuthenticateService,
        UserService,
        TodoService,
        UniversityService,
        FaqService,
        ApplicationsService,
        ApplicationPeriodService,
        CourseCoordinatorService,
        AdministratorService,
        ViewApplicationsService,
        FinalFormsService,
    )

    authenticate_service = AuthenticateService(User, Role)
    user_service = UserService(User)
    todo_service = TodoService(User, Todo)
    course_coordinator_service = CourseCoordinatorService(User, Course)
    university_service = UniversityService(University)
    applications_service = ApplicationsService(user_table=User, application_table=Applications)
    application_period_service = ApplicationPeriodService(User, ApplicationPeriod)
    faq_service = FaqService(user_table=User, faq_table=Faq)
    administrator_service = AdministratorService(User)
    view_applications_service = ViewApplicationsService(User)
    final_forms_service = FinalFormsService(User)

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
        ErasmusCoordinatorHome,
        ErasmusCoordinatorApplications,
        CourseCoordinatorController,
        TodoController,
        FaqFormController,
        InternationalOffice,
        AdministratorController,
        ViewApplicationsController,
        FinalFormsController
    )

    app.add_url_rule("/login/", view_func=Login.as_view("login", authenticate_service=authenticate_service))
    app.add_url_rule(
        "/main/", view_func=Main.as_view("main", university_service=university_service)
    )
    app.add_url_rule("/faq/", view_func=FAQ.as_view("faq", faq_service=faq_service))
    app.add_url_rule(
        "/contacts/", view_func=Contacts.as_view("contacts", user_service=user_service)
    )

    app.add_url_rule(
        "/student_home/", view_func=StudentHome.as_view("student_home", role="Student")
    )
    app.add_url_rule(
        "/student_application/",
        view_func=StudentApplication.as_view(
            "student_application",
            role="Student",
            university_service=university_service,
            applications_service=applications_service,
        ),
    )
    app.add_url_rule(
        "/student_learning_agreement/",
        view_func=LearningAggrementController.as_view(
            "student_learning_agreement",
            role="Student",
            applications_service=applications_service,
        ),
    )
    app.add_url_rule(
        "/student_preapproval/",
        view_func=PreApprovalController.as_view(
            "student_preapproval",
            role="Student",
            applications_service=applications_service,
            course_service="",
        ),
    )
    app.add_url_rule(
        "/ec/home",
        view_func=ErasmusCoordinatorHome.as_view(
            "erasmus_coordinator_homepage",
            role="Erasmus Coordinator",
            user_service=user_service,
            application_period_service=application_period_service,
        ),
    )
    app.add_url_rule(
        "/ec/applications/",
        view_func=ErasmusCoordinatorApplications.as_view(
            "erasmus_coordinator_applications",
            application_period_id=None,
            role="Erasmus Coordinator",
            user_service=user_service,
            applications_service=applications_service,
            application_period_service=application_period_service,
        ),
    )
    app.add_url_rule(
        "/cchome/",
        view_func=CourseCoordinatorController.as_view(
            "course_coordinator_homepage",
            role="Course Coordinator",
            course_coordinator_service=course_coordinator_service,
        ),
    )
    app.add_url_rule(
        "/todo/",
        view_func=TodoController.as_view(
            "todo_page", role="Course Coordinator", todo_service=todo_service
        ),
    )

    app.add_url_rule(
        "/faq/update/department=<department>",
        view_func=FaqFormController.as_view(
            "faq_form",
            role="Erasmus Coordinator",
            user_service=user_service,
            faq_service=faq_service,
        ),
    )
    app.add_url_rule(
        "/intoff/",
        view_func=InternationalOffice.as_view("view_applications", role="International Office"),
    )
    app.add_url_rule(
        "/administrator_homepage",
        view_func=AdministratorController.as_view(
            "administrator_homepage",
            role="Administrator",
            administrator_service=administrator_service,
        ),
    )
    app.add_url_rule(
        "/administrator_view_applications",
        view_func=ViewApplicationsController.as_view(
            "administrator_view_applications",
            role="Administrator",
            view_applications_service=view_applications_service,
        ),
    )
    app.add_url_rule(
        "/final_forms",
        view_func=FinalFormsController.as_view(
            "final_forms", role="Administrator", final_forms_service=final_forms_service
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
