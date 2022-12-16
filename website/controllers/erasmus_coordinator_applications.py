from flask import flash, render_template, request, redirect, url_for, send_file
from flask_login import current_user, login_required, login_user, logout_user
from flask.views import MethodView

from website.services import AuthorizeService
class ErasmusCoordinatorApplications(MethodView, AuthorizeService):
    def __init__(self, role: str, user_service, application_period_service, applications_service, application_period_id, university_service):
        AuthorizeService.__init__(self, role=role)
        self.user_service = user_service
        self.application_period_service = application_period_service
        self.applications_service = applications_service
        self.application_period_id = application_period_id
        self.university_service = university_service

    @login_required
    def get(self):
        if AuthorizeService.is_authorized(self):
            universities = self.university_service.getUniversitiesByDepartment(current_user.department)
            departments = self.university_service.getDepartments(current_user.department)
            university_dictionary = dict(zip(universities, departments))
            return render_template(
                "erasmus_coordinator_applications.html", 
                application_period_id=self.application_period_id, 
                user = current_user, user_service=self.user_service, 
                applications_service=self.applications_service, 
                application_period_service=self.application_period_service,
                university_dictionary=university_dictionary)   
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))
        

    def post(self):
        if AuthorizeService.is_authorized(self): 
            if "application_period_get" in request.form:
                app_period_id = request.form.get("application_period_id")
                self.applications_service.getApplicationsByApplicationPeriodId(app_period_id)
                universities = self.university_service.getUniversitiesByDepartment(current_user.department)
                departments = self.university_service.getDepartments(current_user.department)
                university_dictionary = dict(zip(universities, departments))
                return render_template("erasmus_coordinator_applications.html", application_period_id=app_period_id, user = current_user, university_dictionary=university_dictionary, user_service=self.user_service, applications_service=self.applications_service, application_period_service=self.application_period_service)
            if "download" in request.form:
                application_id = request.form.get("download")
                application = self.applications_service.getApplicationById(application_id)
                status = application.application_status
                if status == "applied" or status == "placed" or status == "waiting bin":
                    applicationPath = self.applications_service.sendApplicationForm(id = application_id)
                    return send_file(applicationPath, as_attachment=True, download_name=str(application.student_id) + "_application_form.pdf")
                if status == "waiting preapproval approval" or status == "preapproval approved":
                    preapprovalPath = self.applications_service.sendPreapprovalForm(id = application_id)
                    return send_file(preapprovalPath, as_attachment=True, download_name=str(application.student_id) + "_pre_approval_form.pdf")
                if status == "waiting learning agreement approval" or status == "ready for mobility":
                    laPath = self.applications_service.sendLearningAgreementForm(id = application_id)
                    return send_file(laPath, as_attachment=True, download_name=str(application.student_id) + "_learning_agreement_form.pdf")
            if "approve" in request.form:
                app_period_id = self.application_period_id
                application_id = request.form.get("approve")
                application = self.applications_service.getApplicationById(id=application_id)
                status = application.application_status
                if status == "waiting preapproval approval":
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="preapproval approved")
                if status == "waiting learning agreement approval":
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="ready for mobility")
                return render_template("erasmus_coordinator_applications.html", application_period_id=app_period_id, user = current_user, user_service=self.user_service, applications_service=self.applications_service, application_period_service=self.application_period_service)
            if "reject" in request.form:
                app_period_id = self.application_period_id
                application_id = request.form.get("reject")
                application = self.applications_service.getApplicationById(id=application_id)
                status = application.application_status
                if status == "waiting preapproval approval":
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="placed")
                if status == "waiting learning agreement approval":
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="preapproval approved")
                return render_template("erasmus_coordinator_applications.html", application_period_id=app_period_id, user = current_user, user_service=self.user_service, applications_service=self.applications_service, application_period_service=self.application_period_service)
            if "place" in request.form:
                app_period_id = self.application_period_id
                application_id = request.form.get("place")
                application = self.applications_service.getApplicationById(id=application_id)
                selected_university_name = request.form.get("select_university")
                university = self.university_service.getUniversityByName(selected_university_name)
                if university != None:
                    department = self.university_service.getDepartment(
                        department=current_user.department,
                        university_id=university.university_id
                    )
                    self.university_service.updateDepartment(
                        department=current_user.department,
                        total_quota=department.total_quota,
                        remaining_quota=department.remaining_quota-1,
                        university_id=university.university_id
                    )
                    self.applications_service.changeApplicationStatus(student_id=application.student_id, status="placed")
                    self.applications_service.matchWithUniversity(student_id=application.student_id, university_id=university.university_id)
                return render_template("erasmus_coordinator_applications.html", application_period_id=app_period_id, user = current_user, user_service=self.user_service, applications_service=self.applications_service, application_period_service=self.application_period_service)
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))