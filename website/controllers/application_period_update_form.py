import datetime
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView
from website.dtos.applicationPeriodUpdateRequest import ApplicationPeriodUpdateRequest

from website.services import AuthorizeService
class ApplicationPeriodUpdateForm(MethodView):
    decorators = [login_required]

    def __init__(self, role: str, user_service, application_period_service):
        AuthorizeService.__init__(self, role=role)
        self.application_period_service = application_period_service
        self.user_service = user_service
    
    def get(self, application_period_id):
        if AuthorizeService.is_authorized(self):
            return render_template(
                "application_period_update.html", 
                user = current_user, 
                user_service=self.user_service,
                application_period_service=self.application_period_service,
                application_period_id=request.view_args["application_period_id"])        
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))
    
    def post(self, application_period_id):
        if AuthorizeService.is_authorized(self):
            if "application_period_create" in request.form:
                title = request.form.get('application_period_update_title')
                status = request.form.get('application_period_update_status')
                print(status)
                deadline = request.form.get('application_period_update_deadline')
                if deadline.__len__() > 0:
                    deadline = datetime.datetime.strptime(deadline, "%d/%m/%y %H.%M")
                else:
                    deadline = None
                
                id = request.view_args["application_period_id"]
                ap_request = ApplicationPeriodUpdateRequest(title=title,status=status,deadline=deadline)
                self.application_period_service.updateApplicationPeriod(id, ap_request)
                return redirect(url_for("erasmus_coordinator_homepage"))
            else:
                return redirect(url_for("erasmus_coordinator_homepage"))
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))