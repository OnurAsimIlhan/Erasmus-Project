from flask_login import login_required, logout_user
from flask import render_template, request, redirect, url_for
from flask.views import MethodView

from website.services import AuthorizeService
class StudentApplication(MethodView, AuthorizeService):
    decorators = [login_required]
    
    def __init__(self, role: str, university_service, applications_service):
        AuthorizeService.__init__(self, role=role)
        self.university_service = university_service
        self.applications_service = applications_service
    
    def get(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
        
        return render_template("student_application_page.html", name="Emirkan")
    
    def post(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
        
        # To be added with the service functionalities