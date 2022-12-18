from flask_login import login_required, current_user, logout_user
from flask import render_template, request, redirect, url_for, send_file
from flask.views import MethodView

from website.services import AuthorizeService


class PreApprovalController(MethodView, AuthorizeService):
    decorators = [login_required]

    def __init__(
        self, role: str, applications_service, course_service, university_service, pdf_service
    ):
        AuthorizeService.__init__(self, role=role)
        self.applications_service = applications_service
        self.course_service = course_service
        self.university_service = university_service
        self.pdf_service = pdf_service

    def get(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

        try:
            if request.args["download"] == "preapproval":
                preapproval_form = self.pdf_service.get_preapproval_form(student_id=current_user.bilkent_id)
                return send_file(preapproval_form, as_attachment=True, download_name="preapproval_form_template.pdf")
        except:
            pass
            
        universities = self.university_service.getAllUniversities()
        return render_template(
            "student_preapproval_page.html", user=current_user, universities=universities
        )

    def post(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

        universities = self.university_service.getAllUniversities()

        if "Choose" in request.form:
            course_id = request.form["Choose"]
            self.applications_service.addCourse(
                student_id=current_user.bilkent_id, course_id=course_id
            )
            self.pdf_service.create_preapproval_form(
                current_user=current_user,
                course_selections=self.applications_service.getSelectedCourses(
                    current_user.bilkent_id
                ),
            )
        
            return render_template(
                "student_preapproval_page.html", user=current_user, universities=universities
            )

        if "Download" in request.form:
            preapproval_form_template = self.pdf_service.get_preapproval_form(current_user.bilkent_id)
            return send_file(preapproval_form_template, as_attachment=True, download_name="preapproval_form_template.pdf")
