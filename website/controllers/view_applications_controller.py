from flask import render_template, redirect, url_for, request, send_file, views
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView

class ViewApplicationsController(MethodView):
    decorators = [login_required]

    def __init__(self, auth_service, view_applications_service):
        self.auth_service = auth_service
        self.view_applications_service = view_applications_service

    def get(self):
        if self.auth_service.is_authorized(user = current_user, required_role = "Administrator"):
            return render_template("view_applications.html", user = current_user)
        else:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))

    def post(self):
        if self.auth_service.is_authorized(user = current_user, required_role = "Administrator"):
            if "logout" in request.form:
                logout_user()
                return redirect(url_for("login"))
        else:
            logout_user()
            return redirect(url_for("your_are_not_authorized_page"))
