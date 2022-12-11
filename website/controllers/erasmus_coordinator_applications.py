from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView

from website.services import AuthorizeService
class ErasmusCoordinatorApplications(MethodView, AuthorizeService):
    def __init__(self, role: str, user_service, application_period_service, applications_service, application_period_id):
        AuthorizeService.__init__(self, role=role)
        self.user_service = user_service
        self.application_period_service = application_period_service
        self.applications_service = applications_service
        self.application_period_id = application_period_id

    @login_required
    def get(self):
        """
        Normalinde application_period bir "optional parameter" olmalı ama onun için flaska ayrı requirement gerekiyo
        şimdilik böyle olsun iş yapıyor
        """
        if AuthorizeService.is_authorized(self):
            return render_template("erasmus_coordinator_applications.html", application_period_id=self.application_period_id, user = current_user, user_service=self.user_service, applications_service=self.applications_service, application_period_service=self.application_period_service)   
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))
        

    def post(self):
        if AuthorizeService.is_authorized(self): 
            if "application_period_get" in request.form:
                app_period_id = request.form.get("application_period_id")
                self.applications_service.getApplicationsByApplicationPeriodId(app_period_id)
                return render_template("erasmus_coordinator_applications.html", application_period_id=app_period_id, user = current_user, user_service=self.user_service, applications_service=self.applications_service, application_period_service=self.application_period_service)
            else:
                logout_user() 
                return redirect(url_for("your_are_not_authorized_page"))