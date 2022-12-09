from flask import render_template, redirect, url_for
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView

from website.services import AuthorizeService
class InternationalOffice(MethodView, AuthorizeService):
    decorators = [login_required]
    
    def __init__(self, role: str):
        AuthorizeService.__init__(self, role=role)

    def get(self):
        if AuthorizeService.is_authorized(self):
            return render_template("view_applications.html", user=current_user)
        else:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
