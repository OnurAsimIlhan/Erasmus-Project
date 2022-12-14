from flask_login import login_required, current_user, logout_user
from flask import render_template, request, redirect, url_for
from flask.views import MethodView

from website.services import AuthorizeService


class StudentHome(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(self, role: str, deadline_service, applications_service):
        AuthorizeService.__init__(self, role=role)
        self.deadline_service = deadline_service
        self.applications_service = applications_service

    def get(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

        application_deadline_bool = self.deadline_service.has_passed("application_deadline")
        preapproval_deadline_bool = self.deadline_service.has_passed("preapproval_deadline")
        learning_agreement_deadline_bool = self.deadline_service.has_passed(
            "learning_agreement_deadline"
        )

        matched_university = self.applications_service.getApplicationByStudentId(
            current_user.bilkent_id
        ).matched_university
        if matched_university == None:
            matched_university = "waiting_bin"

        return render_template(
            "student_homepage.html",
            name=current_user.name,
            application_deadline=application_deadline_bool,
            preapproval_deadline=preapproval_deadline_bool,
            learning_agreement_deadline=learning_agreement_deadline_bool,
            matched_university=matched_university
        )
