from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView
from website.dtos.faqUpdateRequest import FaqUpdateRequest

from website.services.faq_service import FaqService
from website.services.user_service import UserService

class FaqFormController(MethodView):
    def __init__(self, auth_service,  user_service, faq_service):
        self.auth_service = auth_service
        self.faq_service = faq_service
        self.user_service = user_service

    @login_required
    def get(self, department):
        if self.auth_service.is_authorized(user=current_user, required_role="Erasmus Coordinator"):
            return render_template("faq_form.html", user = current_user, faq_service = self.faq_service, user_service=self.user_service)        
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))
    """
        ÖNEMLİ: ÖRNEK SERVİS KULLANIMI: RENDER TEMPLATE'E GEREKEN SERVİSLERİ VER. 
        erasmus_coordinator_home.html'DE KULLANIMI MEVCUT
    """
    def post(self, department):
        if self.auth_service.is_authorized(user=current_user, required_role="Erasmus Coordinator"):
            if "update_faq" in request.form:
                info = request.form.get('update_faq_info')
                user_department = request.view_args["department"]
                if user_department != None:
                    faq_update_request = FaqUpdateRequest(department=user_department, info=info)
                    self.faq_service.updateFaq(user_department, faq_update_request=faq_update_request)
                    return redirect(url_for("erasmus_coordinator_homepage"))
                else:
                    logout_user() 
                    return redirect(url_for("your_are_not_authorized_page"))