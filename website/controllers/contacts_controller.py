from flask import render_template, request, redirect, url_for

from flask.views import MethodView


class Contacts(MethodView):
    def __init__(self, user_service):
        self.user_service = user_service

    def get(self):
        return render_template("contacts_page.html", boolean=True, contacts_list = self.user_service.getAllUsers())
    
    
