from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView
from website.services.application_period_service import ApplicationPeriodService
from website.services.faq_service import FaqService

from website.services import AuthorizeService
class ErasmusCoordinatorHome(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(self, role: str, application_period_service, user_service):
        print("HEREs")
        AuthorizeService.__init__(self, role=role)
        self.application_period_service = application_period_service
        self.user_service = user_service

    
    @login_required
    def get(self):
        if AuthorizeService.is_authorized(self):
            return render_template("erasmus_coordinator_home.html", user = current_user, application_period_service = self.application_period_service, user_service=self.user_service)        
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))
    
    def post(self):
        if AuthorizeService.is_authorized(self):
            if "update_faq" in request.form:
                return redirect(url_for("faq_form", user=current_user))
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))