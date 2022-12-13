from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView
from website.dtos.faqCreateRequest import FaqCreateRequest
from website.dtos.faqUpdateRequest import FaqUpdateRequest

from website.services.faq_service import FaqService
from website.services.user_service import UserService

from website.services import AuthorizeService
class FaqFormController(MethodView):
    decorators = [login_required]

    def __init__(self, role: str, user_service, faq_service):
        AuthorizeService.__init__(self, role=role)
        self.faq_service = faq_service
        self.user_service = user_service

    def get(self, department):
        if AuthorizeService.is_authorized(self):
            return render_template(
                "faq_form.html", 
                user = current_user, 
                faq_service = self.faq_service, 
                user_service=self.user_service)        
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))
            
    def post(self, department):
        if AuthorizeService.is_authorized(self):
            
            if "faq_update" in request.form:
                faq_id = str(request.form.get('faq_update'))
                question = request.form.get('faq_update_question'+faq_id)
                answer = request.form.get('faq_update_answer'+faq_id)
                user_department = request.view_args["department"]

                if user_department != None:
                    faq_update_request = FaqUpdateRequest(department=user_department, question=question, answer=answer)
                    self.faq_service.updateFaq(int(faq_id), faq_update_request)
                    return redirect(url_for("faq_form", user=current_user, department=department))
                else:
                    return redirect(url_for("your_are_not_authorized_page"))
            
            elif "faq_delete" in request.form:
                self.faq_service.deleteFaq(id=request.form.get('faq_delete'))
                return redirect(url_for("faq_form", user=current_user, department=department))
            
            elif "faq_create" in request.form:
                question = request.form.get('faq_create_question')
                answer = request.form.get('faq_create_answer')
                user_department = request.view_args["department"]
                if user_department != None:
                    faq_update_request = FaqCreateRequest(department=user_department, question=question, answer=answer)
                    self.faq_service.addFaq(user_department, faq_update_request)
                return redirect(url_for("faq_form", user=current_user, department=department))
            
            else:
                return redirect(url_for("your_are_not_authorized_page"))