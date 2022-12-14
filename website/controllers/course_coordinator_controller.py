from flask import render_template, redirect, url_for, request, send_file, views
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView

from website.services import AuthorizeService
class CourseCoordinatorController(MethodView, AuthorizeService):
    decorators = [login_required]
    
    def __init__(self, role: str, course_service):
        AuthorizeService.__init__(self, role=role)
        self.course_service = course_service
   

    def get(self):
        if AuthorizeService.is_authorized(self):
            return render_template("course_coordinator_homepage.html", 
                                    user = current_user, 
                                    getBilkentCourseName = self.course_service.getBilkentCourseName,
                                    getUniversityName = self.course_service.getUniversityName)           
        else:
            logout_user() 
            return redirect(url_for("main"))  # not authorized page eklenince değiştirilecek
    
    def post(self):
        if AuthorizeService.is_authorized(self):
            if "Download" in request.form:
                course_id = request.form.get('Download')
                syllabusPath = self.course_service.sendSyllabus(course_id)
                return send_file(syllabusPath, as_attachment=True, download_name= "" + course_id + "_syllabus.pdf")
            if "Approve" in request.form:
                course_id = request.form.get('Approve')
                self.course_service.approveCourse(course_id)
                return redirect(url_for("course_coordinator_homepage", user = current_user)) 
            if "Reject" in request.form:
                course_id = request.form.get('Reject')
                self.course_service.rejectCourse(course_id)
                return redirect(url_for("course_coordinator_homepage", user = current_user)) 
            if "logout" in request.form:
                logout_user() 
                return redirect(url_for("main")) 

        else:
            logout_user() 
            return redirect(url_for("main"))  # not authorized page eklenince değiştirilecek
             
            
        