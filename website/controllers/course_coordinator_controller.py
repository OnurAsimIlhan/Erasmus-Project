from flask import render_template, redirect, url_for, request, send_file, views
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView

from website.services import AuthorizeService
class CourseCoordinatorController(MethodView, AuthorizeService):
    def __init__(self, role: str, course_coordinator_service):
        AuthorizeService.__init__(self, role=role)
        self.course_coordinator_service = course_coordinator_service
   

    @login_required
    def get(self):
        if AuthorizeService.is_authorized(self):
            return render_template("course_coordinator_homepage.html", user = current_user)           
        else:
            logout_user() 
            return redirect(url_for("main"))  # not authorized page eklenince değiştirilecek
    
    @login_required
    def post(self):
        if AuthorizeService.is_authorized(self):
            if "Download" in request.form:
                course_id = request.form.get('Download')
                syllabusPath = self.course_coordinator_service.sendSyllabus(course_id)
                return send_file(syllabusPath, as_attachment=True)
            if "Approve" in request.form:
                course_id = request.form.get('Approve')
                self.course_coordinator_service.approveCourse(course_id)
                return redirect(url_for("course_coordinator_homepage", user = current_user)) 
            if "Reject" in request.form:
                course_id = request.form.get('Reject')
                self.course_coordinator_service.rejectCourse(course_id)
                return redirect(url_for("course_coordinator_homepage", user = current_user)) 
            if "Message" in request.form:
                student_id = request.form.get('Message')
                return redirect(url_for("course_coordinator_homepage", user = current_user)) # message homepage ver service eklenecek
            if "logout" in request.form:
                logout_user() 
                return redirect(url_for("main")) 

        else:
            logout_user() 
            return redirect(url_for("main"))  # not authorized page eklenince değiştirilecek
             
            
        