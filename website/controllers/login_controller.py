from flask import render_template, request, redirect, url_for
from flask.views import MethodView


class Login(MethodView):
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def get(self):
        return render_template("login_page.html", boolean=True)
    
    def post(self):
        try:
            bilkent_id = int(request.form.get("bilkent_id"))
            password = str(request.form.get("password"))
            
            user, role = self.auth_service.authenticate(bilkent_id=bilkent_id, password=password)
            
            # To be Continued...
            return render_template("login_page.html", boolean=True)
        except:
            return render_template("login_page.html", boolean=True)

