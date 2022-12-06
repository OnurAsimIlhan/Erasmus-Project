from flask import render_template, request, redirect, url_for

from flask.views import MethodView


class Main(MethodView):
    def __init__(self, university_service):
        self.university_service = university_service


    def get(self):
        return render_template("main_page.html", boolean=True, university_list = self.university_service.getAllUniversities())
    
    
