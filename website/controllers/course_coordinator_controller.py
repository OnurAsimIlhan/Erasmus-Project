from flask import render_template, redirect, url_for
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView


class CourseCoordinatorController(MethodView):
    def __init__(self, auth_service):
        self.auth_service = auth_service
   

    @login_required
    def get(self):
        if self.auth_service.is_authorized(user=current_user, required_role="Course Coordinator"):
            return render_template("course_coordinator_homepage.html", user = current_user)           
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))  
        