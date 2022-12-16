from flask import render_template, request, redirect, url_for, send_file
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView
# from website.services.application_period_service import ApplicationPeriodService
from website.services.faq_service import FaqService

from website.services import AuthorizeService
class ErasmusCoordinatorHome(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(self, role: str, user_service, applications_service):
        AuthorizeService.__init__(self, role=role)
        self.user_service = user_service
        self.applications_service = applications_service

    def get(self):
        if AuthorizeService.is_authorized(self):
            
            # all applications by department
            applications = self.applications_service.getApplicationsByDepartment(current_user.department)

            return render_template(
                "erasmus_coordinator_home.html", 
                user = current_user, 
                user_service = self.user_service,
                applications = applications
                )        
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))
    
    def post(self):
        if AuthorizeService.is_authorized(self):
            if "update_faq" in request.form:
                return redirect(url_for("faq_form", user=current_user))
            if "application_form" in request.form:
                application_id = request.form.get("application_form")
                application = self.applications_service.getApplicationById(application_id)
                applicationPath = self.applications_service.sendApplicationForm(id = application_id)
                return send_file(applicationPath, as_attachment=True, download_name=str(application.student_id) + "_application_form.pdf")
            if "pre_approval" in request.form:
                application_id = request.form.get("pre_approval")
                application = self.applications_service.getApplicationById(application_id)
                preapprovalPath = self.applications_service.sendPreapprovalForm(id = application_id)
                return send_file(preapprovalPath, as_attachment=True, download_name=str(application.student_id) + "_pre_approval_form.pdf")
            if "learning_agreement" in request.form:
                application_id = request.form.get("learning_agreement")
                application = self.applications_service.getApplicationById(application_id)
                laPath = self.applications_service.sendLearningAgreementForm(id = application_id)
                return send_file(laPath, as_attachment=True, download_name=str(application.student_id) + "_learning_agreement_form.pdf")
            if "approve" in request.form:
                application_id = request.form.get("approve")
                application = self.applications_service.getApplicationById(id=application_id)
                # app_period_id = application.application_period_id
                status = application.application_status
                if status == "waiting preapproval approval":
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="preapproval approved")
                if status == "waiting learning agreement approval":
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="ready for mobility")
                applications = self.applications_service.getApplicationsByDepartment(current_user.department)
                return render_template("erasmus_coordinator_home.html", user = current_user, applications=applications)

                # return render_template("erasmus_coordinator_applications.html", application_period_id=app_period_id, user = current_user, university_dictionary=university_dictionary, user_service=self.user_service, applications_service=self.applications_service, application_period_service=self.application_period_service)
            if "reject" in request.form:
                application_id = request.form.get("reject")
                application = self.applications_service.getApplicationById(id=application_id)
                # app_period_id = application.application_period_id
                status = application.application_status
                if status == "waiting preapproval approval":
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="placed")
                if status == "waiting learning agreement approval":
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="preapproval approved")
                applications = self.applications_service.getApplicationsByDepartment(current_user.department)
                return render_template("erasmus_coordinator_home.html", user = current_user, applications=applications)
            
                
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))