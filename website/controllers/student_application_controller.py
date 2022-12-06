from flask_login import login_required, current_user, logout_user
from flask import render_template, request, redirect, url_for
from flask.views import MethodView

class StudentApplication(MethodView):
    decorators = [login_required]
    
    def __init__(self, auth_service, university_service, applications_service):
        self.auth_service = auth_service
        self.university_service = university_service
        self.applications_service = applications_service
    
    def get(self):
        if self.auth_service.is_authorized(user=current_user, required_role="student") == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
        
        return render_template("student_application_page.html", name="Emirkan")
    
    def post(self):
        if self.auth_service.is_authorized(user=current_user, required_role="student") == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
        
        # To be added with the service functionalities