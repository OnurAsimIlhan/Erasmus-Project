from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView


class ErasmusCoordinatorViewApplications(MethodView):
    def __init__(self, auth_service, application_service):
        self.auth_service = auth_service
        self.application_service = application_service

    @login_required
    def get(self):
        if self.auth_service.is_authorized(user=current_user, required_role="Erasmus Coordinator"):
            return render_template("erasmus_coordinator_applications.html", user = current_user, application_service = self.application_service)        
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))  
    
    def post(self):
        pass