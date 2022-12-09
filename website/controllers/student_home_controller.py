from flask_login import login_required, current_user, logout_user
from flask import render_template, request, redirect, url_for
from flask.views import MethodView

from website.services import AuthorizeService
class StudentHome(MethodView, AuthorizeService):
    decorators = [login_required]
    
    def __init__(self, role: str):
        AuthorizeService.__init__(self, role=role)
    
    def get(self):
        if AuthorizeService.is_authorized(self) == False:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
        
        return render_template("student_homepage.html", name=current_user.name)