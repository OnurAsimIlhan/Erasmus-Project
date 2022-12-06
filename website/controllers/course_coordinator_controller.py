from flask import render_template, redirect, url_for, request, send_file, views
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView


class CourseCoordinatorController(MethodView):
    def __init__(self, auth_service, course_coordinator_service):
        self.auth_service = auth_service
        self.course_coordinator_service = course_coordinator_service
   

    @login_required
    def get(self):
        if self.auth_service.is_authorized(user=current_user, required_role="Course Coordinator"):
            return render_template("course_coordinator_homepage.html", user = current_user)           
        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))  
    
    @login_required
    def post(self):
        if self.auth_service.is_authorized(user=current_user, required_role="Course Coordinator"):
            if "download" in request.form:
                course_id = request.form.get('download')
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
            if "home" in request.form:
                return redirect(url_for("course_coordinator_homepage", user = current_user)) 
            if "todo" in request.form:
                return redirect(url_for("todo_page", user = current_user))
            if "logout" in request.form:
                logout_user() 
                return redirect(url_for("login"))

        else:
            logout_user() 
            return redirect(url_for("your_are_not_authorized_page"))  
             
            
        