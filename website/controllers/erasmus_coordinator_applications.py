from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView


class ErasmusCoordinatorApplications(MethodView):
    def __init__(self, auth_service, user_service, applications_service, application_period_service, application_period_id):
        self.auth_service = auth_service
        self.applications_service = applications_service
        self.user_service = user_service
        self.application_period_service = application_period_service
        self.application_period_id = application_period_id

    @login_required
    def get(self):
        """
        Normalinde application_period bir "optional parameter" olmalı ama onun için flaska ayrı requirement gerekiyo
        şimdilik böyle olsun iş yapıyor
        """
        if self.auth_service.is_authorized(user=current_user, required_role="Erasmus Coordinator"):
            return render_template("erasmus_coordinator_applications.html", application_period_id=self.application_period_id, user = current_user, user_service=self.user_service, applications_service=self.applications_service, application_period_service=self.application_period_service)   
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))
        

    def post(self):
        if self.auth_service.is_authorized(user=current_user, required_role="Erasmus Coordinator"): 
            if "application_period_get" in request.form:
                app_period_id = request.form.get("application_period_id")
                self.applications_service.getApplicationsByApplicationPeriodId(app_period_id)
                return render_template("erasmus_coordinator_applications.html", application_period_id=app_period_id, user = current_user, user_service=self.user_service, applications_service=self.applications_service, application_period_service=self.application_period_service)
            else:
                logout_user() 
                return redirect(url_for("your_are_not_authorized_page"))