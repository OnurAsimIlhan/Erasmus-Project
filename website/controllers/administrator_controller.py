from flask import render_template, redirect, url_for, request, send_file, views
from flask_login import login_required, current_user, logout_user
from flask.views import MethodView

class AdministratorController(MethodView):
    def __init__(self, auth_service, administrator_service):
        self.auth_service = auth_service
        self.administrator_service = administrator_service

    @login_required
    def get(self):
        if self.auth_service.is_authorized(user = current_user, required_role = "Administrator"):
            return render_template("administrator_homepage.html", user = current_user)
        else:
            logout_user
            return redirect(url_for("your_are_not_authorized_page"))

    @login_required
    def post(self):
        if self.auth_service.is_authorized(user = current_user, required_role = "Administrator"):
            pass
        else:
            logout_user
            return redirect(url_for("your_are_not_authorized_page"))