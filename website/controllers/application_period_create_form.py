import datetime
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView
from website.dtos.applicationPeriodCreateRequest import ApplicationPeriodCreateRequest

from website.services import AuthorizeService
class ApplicationPeriodCreateForm(MethodView):
    decorators = [login_required]

    def __init__(self, role: str, user_service, application_period_service):
        AuthorizeService.__init__(self, role=role)
        self.application_period_service = application_period_service
        self.user_service = user_service
    
    def get(self, department):
        if AuthorizeService.is_authorized(self):
            return render_template(
                "application_period_form.html", 
                user = current_user, 
                user_service=self.user_service,
                application_period_service=self.application_period_service)        
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))
    
    def post(self, department):
        if AuthorizeService.is_authorized(self):
            if "application_period_create" in request.form:
                title = request.form.get('application_period_create_title')
                type = request.form.get('application_period_create_type')
                user_department = request.view_args["department"]
                ap_request = ApplicationPeriodCreateRequest(department=user_department,title=title,type=type)
                self.application_period_service.addApplicationPeriod(ap_request)
                return redirect(url_for("erasmus_coordinator_homepage"))
            else:
                return redirect(url_for("erasmus_coordinator_homepage"))
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))

