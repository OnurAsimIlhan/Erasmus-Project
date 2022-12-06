from flask_login import login_required, current_user, logout_user
from flask import render_template, request, redirect, url_for
from flask.views import MethodView

class StudentHome(MethodView):
    decorators = [login_required]
    
    def __init__(self, auth_service):
        self.auth_service = auth_service
    
    def get(self):
        if self.auth_service.is_authorized(user=current_user, required_role="student") == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
        
        return render_template("student_homepage.html", name=current_user.name)