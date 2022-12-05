from website import db
from website.models import Application

class ApplicationService():
    def __init__(self, user_table, application_table):
        self.user_table = user_table
        self.application_table = application_table
    
    def getApplicationById(self, id: int):
        task = self.application_table.query.filter_by(id = id).first()
        print(task)
        return task

    def getApplicationsByDepartment(self, dep: str):
        applications = self.application_table.query.filter_by(deparment = dep).all()
        return applications