from flask_login import login_required, current_user, logout_user
from flask import render_template, request, redirect, url_for
from flask.views import MethodView

from website.services import AuthorizeService

class CourseProposalController(AuthorizeService):
    decorators = [login_required]

    def __init__(self, role, applications_service, university_service, course_service):
        AuthorizeService.__init__(self, role=role)
        self.course_service = course_service
        self.applications_service = applications_service
        self.university_service = university_service

    def get(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))





    def post(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))




