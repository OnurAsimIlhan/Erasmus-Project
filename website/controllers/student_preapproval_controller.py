from flask_login import login_required, current_user, logout_user
from flask import render_template, request, redirect, url_for, send_file
from flask.views import MethodView

from website.services import AuthorizeService
class PreApprovalController(MethodView, AuthorizeService):
    decorators = [login_required]
    
    def __init__(self, role: str,  applications_service, course_service, university_service):
        AuthorizeService.__init__(self, role=role)
        self.applications_service = applications_service
        self.course_service = course_service
        self.university_service = university_service
    
    def get(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

        universities = self.university_service.getAllUniversities()
        courses = self.applications_service.getCourses(student_id=current_user.bilkent_id)
        return render_template("student_preapproval_page.html", user=current_user, universities=universities, courses=courses)
    
    def post(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

        universities = self.university_service.getAllUniversities()

        if "Choose" in request.form:
            course_name = request.form["Choose"]
            self.applications_service.addCourse(student_id=current_user.bilkent_id, course_name=course_name)
            courses = self.applications_service.getCourses(student_id=current_user.bilkent_id)
            return render_template("student_preapproval_page.html", user=current_user, universities=universities, courses=courses)

        #if "Download" in request.form:
         #   downFile = self.applications_service.download(student_id=current_user.bilkent_id)
          #  return send_file(downFile, as_attachment=True)

            # To be added with the service functionalities